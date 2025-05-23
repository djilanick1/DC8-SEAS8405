# Stage 1 - Build
FROM python:3.13-alpine AS builder

WORKDIR /app
COPY . /app
RUN pip install --user -r requirements.txt

# Stage 2 - Runtime
FROM python:3.13-alpine

RUN adduser -D appuser
WORKDIR /app
COPY --from=builder /app /app
COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

USER appuser

HEALTHCHECK --interval=30s --timeout=10s CMD curl -f http://localhost:5000/ || exit 1

CMD ["python", "app.py"]

