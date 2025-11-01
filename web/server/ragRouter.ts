import { publicProcedure, router } from "./_core/trpc";
import { z } from "zod";
import { ragClient } from "./ragClient";
import { TRPCError } from "@trpc/server";

export const ragRouter = router({
  /**
   * Get system statistics from RAG backend
   */
  getStats: publicProcedure.query(async () => {
    try {
      const stats = await ragClient.getStats();
      return {
        documents: stats.documents,
        vectors: stats.vectors,
        embeddingModel: stats.embedding_model,
        device: stats.device,
        status: stats.status as "ready" | "indexing" | "error",
      };
    } catch (error) {
      console.error("Failed to get stats from RAG API:", error);
      // Return fallback stats if API is unavailable
      return {
        documents: 0,
        vectors: 0,
        embeddingModel: "unknown",
        device: "unknown",
        status: "error" as const,
      };
    }
  }),

  /**
   * Query documents using semantic search
   */
  query: publicProcedure
    .input(
      z.object({
        question: z.string().min(1, "Question cannot be empty"),
      })
    )
    .mutation(async ({ input }) => {
      try {
        const response = await ragClient.query(input.question);
        
        if (!response.success) {
          throw new TRPCError({
            code: "INTERNAL_SERVER_ERROR",
            message: response.error || "Query failed",
          });
        }

        return { result: response.result };
      } catch (error) {
        console.error("Query error:", error);
        throw new TRPCError({
          code: "INTERNAL_SERVER_ERROR",
          message: error instanceof Error ? error.message : "Failed to query documents",
        });
      }
    }),

  /**
   * Extract information about specific strength class
   */
  extract: publicProcedure
    .input(
      z.object({
        className: z.string().min(1, "Class name cannot be empty"),
      })
    )
    .mutation(async ({ input }) => {
      try {
        const response = await ragClient.extract(input.className);
        
        if (!response.success) {
          throw new TRPCError({
            code: "INTERNAL_SERVER_ERROR",
            message: response.error || "Extraction failed",
          });
        }

        return { result: response.result };
      } catch (error) {
        console.error("Extract error:", error);
        throw new TRPCError({
          code: "INTERNAL_SERVER_ERROR",
          message: error instanceof Error ? error.message : "Failed to extract class information",
        });
      }
    }),

  /**
   * Check RAG API health status
   */
  healthCheck: publicProcedure.query(async () => {
    try {
      const health = await ragClient.healthCheck();
      return {
        status: health.status,
        message: health.message,
        healthy: health.status === "healthy",
      };
    } catch (error) {
      return {
        status: "error",
        message: error instanceof Error ? error.message : "RAG API unavailable",
        healthy: false,
      };
    }
  }),
});
