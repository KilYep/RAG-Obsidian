import { openai } from "@ai-sdk/openai"
import { streamText } from "ai"

export const runtime = "edge"

export async function POST(req: Request) {
  const { messages } = await req.json()
  const result = streamText({
    model: openai("gpt-4-turbo"),
    messages,
    // 这里可以添加您的RAG逻辑
    // 例如,您可以在这里检索相关的笔记内容,并将其添加到system或user消息中
  })
  return result.toDataStreamResponse()
}

