# Задания (дословно)

Одно сообщение, без системного промпта. Уровень размышлений medium у всех трёх, `max_tokens` 64 000.
MiniMax M3.1 Flash и DeepSeek V4.1 Flash 1017 — через OpenRouter (MiniMax в бесплатном варианте `:free` первых дней), Claude Opus 5.5 — через Anthropic API.

## 1. Семиугольник

```text
Write a single HTML file (no external libraries) that shows 20 balls bouncing inside a spinning heptagon:
- All balls have the same radius. Balls are numbered 1 to 20 and use these colors: #f8b862, #f6ad49, #f39800, #f08300, #ec6d51, #ee7948, #ed6d3d, #ec6800, #ee7800, #eb6238, #ea5506, #eb6101, #e49e61, #e45e32, #e17b34, #dd7a56, #db8449, #d66a35, #c85554, #d9333f.
- The balls drop from the heptagon center when the page starts.
- Balls are affected by gravity and friction, and they must bounce off the rotating walls realistically. There must also be collisions between balls.
- The impact bounce height must not exceed the radius of the heptagon, but must be higher than the ball radius.
- The heptagon spins around its center at 360 degrees per 5 seconds.
- The heptagon must be large enough to contain all the balls.
- Do not use any physics library; implement collision detection and response yourself.
- Balls also rotate because of friction; the number drawn on each ball shows its spin.
Use a 720x720 canvas on a dark background. Return only the code in one ```html``` block.
```

## 2. Пеликан

```text
Generate an SVG of a pelican riding a bicycle. Return only the SVG code in one ```svg``` block.
```
