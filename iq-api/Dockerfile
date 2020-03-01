FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7 as builder

COPY ./app /app/app
COPY ./requirements.txt /app/

WORKDIR /app/
RUN pip install -r requirements.txt --user


FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7 as runner
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app
