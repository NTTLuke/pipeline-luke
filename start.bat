@echo off
set PORT=9099
set HOST=0.0.0.0

REM ADMIN CONNECTION OPENAI API SETTINGS
REM http://host.docker.internal:9099 when running in terminal
REM http://localhost:9099 when running in docker


@REM ORIGINAL SCRIPT
@REM uvicorn main:app --host %HOST% --port %PORT% --forwarded-allow-ips '*'

@REM CUSTOM SCRIPT
uvicorn spotify_auth_routes:app --host %HOST% --port %PORT% --forwarded-allow-ips '*'