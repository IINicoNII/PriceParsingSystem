Write-Host "Starting copying files..." -ForegroundColor Green
 
Invoke-Expression "scp -r C:\Users\vr279\price_parsing\DataBase bot_host@193.124.117.67:/home/bot_host/price_parsing/"
Invoke-Expression "scp -r C:\Users\vr279\price_parsing\Parsing bot_host@193.124.117.67:/home/bot_host/price_parsing/"
Invoke-Expression "scp -r C:\Users\vr279\price_parsing\TGBot bot_host@193.124.117.67:/home/bot_host/price_parsing/"
Invoke-Expression "scp -r C:\Users\vr279\price_parsing\config.py bot_host@193.124.117.67:/home/bot_host/price_parsing/"
Invoke-Expression "scp -r C:\Users\vr279\price_parsing\main.py bot_host@193.124.117.67:/home/bot_host/price_parsing/"
Invoke-Expression "scp -r C:\Users\vr279\price_parsing\setup.py bot_host@193.124.117.67:/home/bot_host/price_parsing/"
Invoke-Expression "scp -r C:\Users\vr279\price_parsing\.env bot_host@193.124.117.67:/home/bot_host/price_parsing/"

# === Проверка результата ===
#if ($LASTEXITCODE -eq 0) {
#    Write-Host "✅ Файлы успешно переданы!" -ForegroundColor Green
#} else {
#    Write-Host "❌ Ошибка при передаче файлов." -ForegroundColor Red
#}

Read-Host "Press enter to exit..."