import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { Search, Upload, Database, Settings, FileText, Cpu, Zap } from "lucide-react";
import { APP_TITLE } from "@/const";
import { Streamdown } from 'streamdown';
import { trpc } from "@/lib/trpc";

export default function Home() {
  const [query, setQuery] = useState("");
  const [className, setClassName] = useState("");
  const [result, setResult] = useState("");

  // Get system stats from backend
  const { data: stats, isLoading: statsLoading } = trpc.rag.getStats.useQuery(undefined, {
    refetchInterval: 10000, // Refresh every 10 seconds
  });

  // Query mutation
  const queryMutation = trpc.rag.query.useMutation({
    onSuccess: (data: { result: string }) => {
      setResult(data.result);
      toast.success("Поиск завершен");
    },
    onError: (error: any) => {
      toast.error(`Ошибка: ${error.message}`);
    },
  });

  // Extract mutation
  const extractMutation = trpc.rag.extract.useMutation({
    onSuccess: (data: { result: string }) => {
      setResult(data.result);
      toast.success("Данные извлечены");
    },
    onError: (error: any) => {
      toast.error(`Ошибка: ${error.message}`);
    },
  });

  const handleQuery = async () => {
    if (!query.trim()) {
      toast.error("Введите запрос");
      return;
    }
    toast.info("Поиск в документах...");
    queryMutation.mutate({ question: query });
  };

  const handleExtract = async () => {
    if (!className.trim()) {
      toast.error("Введите класс прочности");
      return;
    }
    toast.info("Извлечение данных...");
    extractMutation.mutate({ className });
  };

  const handleUpload = () => {
    toast.info("Функция загрузки будет доступна в следующей версии");
  };

  const isLoading = queryMutation.isPending || extractMutation.isPending;
  const defaultStats = {
    documents: 0,
    vectors: 0,
    embeddingModel: "intfloat/multilingual-e5-large",
    device: "cuda",
    status: "ready"
  };
  const displayStats = stats || defaultStats;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-950 dark:to-slate-900">
      {/* Header */}
      <header className="border-b bg-white/80 dark:bg-slate-950/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Database className="h-8 w-8 text-blue-600" />
              <div>
                <h1 className="text-2xl font-bold">{APP_TITLE}</h1>
                <p className="text-sm text-muted-foreground">Анализ документов ГОСТ с помощью RAG</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="outline" className="gap-1">
                <Cpu className="h-3 w-3" />
                {displayStats.device === "cuda" ? "GPU" : "CPU"}
              </Badge>
              <Badge variant="outline" className="gap-1">
                <Zap className="h-3 w-3" />
                {displayStats.status === "ready" ? "Готов" : "Индексация..."}
              </Badge>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Panel - Query Interface */}
          <div className="lg:col-span-2 space-y-6">
            <Tabs defaultValue="query" className="w-full">
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="query" className="gap-2">
                  <Search className="h-4 w-4" />
                  Поиск
                </TabsTrigger>
                <TabsTrigger value="extract" className="gap-2">
                  <FileText className="h-4 w-4" />
                  Извлечение
                </TabsTrigger>
                <TabsTrigger value="upload" className="gap-2">
                  <Upload className="h-4 w-4" />
                  Загрузка
                </TabsTrigger>
              </TabsList>

              <TabsContent value="query" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle>Семантический поиск</CardTitle>
                    <CardDescription>
                      Введите вопрос или запрос для поиска в документах ГОСТ
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <Textarea
                      placeholder="Например: Какие характеристики у класса прочности C235?"
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                      rows={4}
                      className="resize-none"
                    />
                    <Button onClick={handleQuery} disabled={isLoading} className="w-full">
                      {isLoading ? "Поиск..." : "Найти"}
                    </Button>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="extract" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle>Извлечение данных о классе прочности</CardTitle>
                    <CardDescription>
                      Получите полную информацию о конкретном классе прочности
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <Input
                      placeholder="Например: C235"
                      value={className}
                      onChange={(e) => setClassName(e.target.value.toUpperCase())}
                    />
                    <Button onClick={handleExtract} disabled={isLoading} className="w-full">
                      {isLoading ? "Извлечение..." : "Извлечь данные"}
                    </Button>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="upload" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle>Загрузка документов</CardTitle>
                    <CardDescription>
                      Добавьте новые документы ГОСТ для индексации
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="border-2 border-dashed rounded-lg p-12 text-center hover:border-primary/50 transition-colors cursor-pointer">
                      <Upload className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                      <p className="text-sm text-muted-foreground mb-2">Перетащите PDF файлы сюда или</p>
                      <Button onClick={handleUpload} variant="outline">Выбрать файлы</Button>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>

            {/* Results */}
            {result && (
              <Card>
                <CardHeader>
                  <CardTitle>Результаты</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="prose dark:prose-invert max-w-none">
                    <Streamdown>{result}</Streamdown>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Right Panel - Stats & Info */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Database className="h-5 w-5" />
                  Статистика системы
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {statsLoading ? (
                  <p className="text-sm text-muted-foreground">Загрузка...</p>
                ) : (
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Документов:</span>
                      <span className="font-medium">{displayStats.documents}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Векторов:</span>
                      <span className="font-medium">{displayStats.vectors}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Модель:</span>
                      <span className="text-xs font-mono">{displayStats.embeddingModel.split('/')[1]}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm text-muted-foreground">Устройство:</span>
                      <Badge variant={displayStats.device === "cuda" ? "default" : "secondary"}>
                        {displayStats.device.toUpperCase()}
                      </Badge>
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Settings className="h-5 w-5" />
                  О системе
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2 text-sm text-muted-foreground">
                <p>RAG система для анализа технических документов ГОСТ с использованием локальных эмбеддингов и GPU ускорения.</p>
                <div className="pt-4 space-y-1">
                  <p className="font-medium text-foreground">Возможности:</p>
                  <ul className="list-disc list-inside space-y-1 text-xs">
                    <li>Семантический поиск по документам</li>
                    <li>Извлечение структурированных данных</li>
                    <li>Анализ классов прочности стали</li>
                    <li>GPU ускорение (10-50x)</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>
    </div>
  );
}
