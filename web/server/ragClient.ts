/**
 * Client for Python RAG API
 * Handles communication with FastAPI backend
 */

const RAG_API_URL = process.env.RAG_API_URL || "http://localhost:8000";

interface QueryRequest {
  question: string;
}

interface ExtractRequest {
  class_name: string;
}

interface QueryResponse {
  result: string;
  success: boolean;
  error?: string;
}

interface StatsResponse {
  documents: number;
  vectors: number;
  embedding_model: string;
  device: string;
  status: string;
}

interface HealthResponse {
  status: string;
  message: string;
}

class RAGClient {
  private baseUrl: string;

  constructor(baseUrl: string = RAG_API_URL) {
    this.baseUrl = baseUrl;
  }

  /**
   * Check if RAG API is healthy
   */
  async healthCheck(): Promise<HealthResponse> {
    const response = await fetch(`${this.baseUrl}/health`);
    if (!response.ok) {
      throw new Error(`Health check failed: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Get system statistics
   */
  async getStats(): Promise<StatsResponse> {
    const response = await fetch(`${this.baseUrl}/stats`);
    if (!response.ok) {
      throw new Error(`Failed to get stats: ${response.statusText}`);
    }
    return response.json();
  }

  /**
   * Query documents
   */
  async query(question: string): Promise<QueryResponse> {
    const request: QueryRequest = { question };
    const response = await fetch(`${this.baseUrl}/query`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Query failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Extract strength class information
   */
  async extract(className: string): Promise<QueryResponse> {
    const request: ExtractRequest = { class_name: className };
    const response = await fetch(`${this.baseUrl}/extract`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(request),
    });

    if (!response.ok) {
      throw new Error(`Extract failed: ${response.statusText}`);
    }

    return response.json();
  }
}

// Export singleton instance
export const ragClient = new RAGClient();
