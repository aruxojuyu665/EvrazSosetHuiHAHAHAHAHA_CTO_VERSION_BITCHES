/**
 * Client for Python RAG API
 * Handles communication with FastAPI backend
 */

const RAG_API_URL = process.env.RAG_API_URL || "http://localhost:8000";
const REQUEST_TIMEOUT = 60000; // 60 seconds

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
  private timeout: number;

  constructor(baseUrl: string = RAG_API_URL, timeout: number = REQUEST_TIMEOUT) {
    this.baseUrl = baseUrl;
    this.timeout = timeout;
  }

  /**
   * Fetch with timeout
   */
  private async fetchWithTimeout(url: string, options: RequestInit = {}): Promise<Response> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
      });
      clearTimeout(timeoutId);
      return response;
    } catch (error) {
      clearTimeout(timeoutId);
      if (error instanceof Error) {
        if (error.name === 'AbortError') {
          throw new Error(`Request timeout after ${this.timeout}ms`);
        }
        throw new Error(`Network error: ${error.message}`);
      }
      throw error;
    }
  }

  /**
   * Validate response structure
   */
  private validateQueryResponse(data: any): data is QueryResponse {
    return (
      typeof data === 'object' &&
      data !== null &&
      typeof data.result === 'string' &&
      typeof data.success === 'boolean'
    );
  }

  private validateStatsResponse(data: any): data is StatsResponse {
    return (
      typeof data === 'object' &&
      data !== null &&
      typeof data.documents === 'number' &&
      typeof data.vectors === 'number' &&
      typeof data.embedding_model === 'string' &&
      typeof data.device === 'string' &&
      typeof data.status === 'string'
    );
  }

  private validateHealthResponse(data: any): data is HealthResponse {
    return (
      typeof data === 'object' &&
      data !== null &&
      typeof data.status === 'string' &&
      typeof data.message === 'string'
    );
  }

  /**
   * Check if RAG API is healthy
   */
  async healthCheck(): Promise<HealthResponse> {
    try {
      const response = await this.fetchWithTimeout(`${this.baseUrl}/health`);
      if (!response.ok) {
        throw new Error(`Health check failed: ${response.statusText}`);
      }
      const data = await response.json();
      if (!this.validateHealthResponse(data)) {
        throw new Error('Invalid health response structure');
      }
      return data;
    } catch (error) {
      if (error instanceof Error) {
        throw new Error(`Health check failed: ${error.message}`);
      }
      throw error;
    }
  }

  /**
   * Get system statistics
   */
  async getStats(): Promise<StatsResponse> {
    try {
      const response = await this.fetchWithTimeout(`${this.baseUrl}/stats`);
      if (!response.ok) {
        throw new Error(`Failed to get stats: ${response.statusText}`);
      }
      const data = await response.json();
      if (!this.validateStatsResponse(data)) {
        throw new Error('Invalid stats response structure');
      }
      return data;
    } catch (error) {
      if (error instanceof Error) {
        throw new Error(`Get stats failed: ${error.message}`);
      }
      throw error;
    }
  }

  /**
   * Query documents with retry logic
   */
  async query(question: string, retries: number = 2): Promise<QueryResponse> {
    const request: QueryRequest = { question };
    
    for (let attempt = 0; attempt <= retries; attempt++) {
      try {
        const response = await this.fetchWithTimeout(`${this.baseUrl}/query`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(request),
        });

        if (!response.ok) {
          throw new Error(`Query failed: ${response.statusText}`);
        }

        const data = await response.json();
        if (!this.validateQueryResponse(data)) {
          throw new Error('Invalid query response structure');
        }
        
        return data;
      } catch (error) {
        if (attempt === retries) {
          if (error instanceof Error) {
            throw new Error(`Query failed after ${retries + 1} attempts: ${error.message}`);
          }
          throw error;
        }
        // Exponential backoff: 1s, 2s, 4s
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
      }
    }
    
    throw new Error('Query failed: max retries exceeded');
  }

  /**
   * Extract strength class information with retry logic
   */
  async extract(className: string, retries: number = 2): Promise<QueryResponse> {
    const request: ExtractRequest = { class_name: className };
    
    for (let attempt = 0; attempt <= retries; attempt++) {
      try {
        const response = await this.fetchWithTimeout(`${this.baseUrl}/extract`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(request),
        });

        if (!response.ok) {
          throw new Error(`Extract failed: ${response.statusText}`);
        }

        const data = await response.json();
        if (!this.validateQueryResponse(data)) {
          throw new Error('Invalid extract response structure');
        }
        
        return data;
      } catch (error) {
        if (attempt === retries) {
          if (error instanceof Error) {
            throw new Error(`Extract failed after ${retries + 1} attempts: ${error.message}`);
          }
          throw error;
        }
        // Exponential backoff: 1s, 2s, 4s
        await new Promise(resolve => setTimeout(resolve, Math.pow(2, attempt) * 1000));
      }
    }
    
    throw new Error('Extract failed: max retries exceeded');
  }
}

// Export singleton instance
export const ragClient = new RAGClient();
