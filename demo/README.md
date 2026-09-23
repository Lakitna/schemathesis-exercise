# Schemathesis demo

1. Open demo folder in CLI

   ```shell
   cd ./demo
   ```

   Open in vscode

   ```shell
   code .
   ```

2. Show OpenAPI Schema

   ```plain
   ./api/xkcd/schema.openapi.yaml
   ```

3. Start server

   ```shell
   uv run py -m api
   ```

4. Show the server working

   ```shell
   curl -v http://127.0.0.1:5000/info
   curl -v -H "Authorization: Bearer super-secret" http://127.0.0.1:5000/info
   curl -v -H "Authorization: Bearer super-secret" http://127.0.0.1:5000/614/info
   ```

5. Run with Schemathesis CLI while showing server log stream

   Note: Authorization in `./schemathesis.toml`

   ```shell
   uv run st run ./api/xkcd/schema.openapi.yaml --url http://127.0.0.1:5000
   ```

6. Run with pytest while showing server log stream

   ```shell
   uv run pytest test/xkcd.py -vv
   ```

   Show test file

   ```plain
   ./test/xkcd.py
   ```

## Fix the bug

Comment out the following line

```log
./api/xkcd/__init__.py:85
```
