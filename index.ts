import { Hono } from 'hono';
import { handle } from 'hono/vercel';
import { inject } from "@vercel/analytics";
import { injectSpeedInsights } from '@vercel/speed-insights';
 
inject({
});
injectSpeedInsights();

const app = new Hono()
const api = app.basePath('/api')

app.get('/', (c) => {
  return c.json({ message: 'Index!' })
})

api.get('/', (c) => {
  return c.json({ message: 'Hello Hono!' })
})

api.post('/webhooks/:webhookName', async (c) => {
  const webhookName = c.req.param('webhookName')
  const body = await c.req.json()
  const data = {
    webhook: {
      name: webhookName,
      data: body
    }
  }
  const forwardUrl = process.env.FORWARD_URL as string
  if (!forwardUrl) {
    return c.json({ status: 'error', message: 'Missing environment variable: FORWARD_URL' }, 500)
  }
  try {
    const response = await fetch(forwardUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })
    return c.json({
      status: 'ok',
    })
  } catch (error) {
    return c.json({
      status: 'error',
      message: (error as Error).message 
    }, 500)
  }
})

export const config = {
  runtime: 'edge'
}
export default handle(app)
