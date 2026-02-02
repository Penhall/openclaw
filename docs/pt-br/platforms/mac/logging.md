---
summary: "OpenClaw logging: rolling diagnostics file log + unified log privacy flags"
read_when:
  - Capturing macOS logs or investigating private data logging
  - Debugging voice wake/session lifecycle issues
---

# Logging (macOS)

# # Rolling diagnostics file log (Debug pane)

O OpenClaw roteia os logs de aplicativos do macOS através do swift-log (registro unificado por padrão) e pode escrever um log de arquivos local e rotativo no disco quando você precisar de uma captura durável.

- Verbosity: **Painel de depuração → Logs → Registro de aplicativos → Verbosity**
- Activar: **Debug pane → Logs → Registo de aplicações → “Write rolling diagnostics log (JSONL)”**
- Localização: <<CODE0>> (rota automaticamente; arquivos antigos são sufixos com <<CODE1>>, <<CODE2>>, ...)
- Clear: **Debug pane → Logs → App loging → “Limpar”**

Notas:

- Isto é ** off por padrão**. Activar apenas durante a depuração activa.
- Trate o arquivo como sensível; não compartilhe sem revisão.

# # Registro unificado de dados privados no macOS

Registro unificado edita a maioria das cargas úteis, a menos que um subsistema opte por <<CODE0>>. Por Peter's write-up no macOS [logging privacy shenanigans](<<<LINK0>>) (2025) isso é controlado por uma plist em <<CODE1>>> Teclado pelo nome do subsistema. Apenas entradas de log novas captam a bandeira, então habilite-a antes de reproduzir um problema.

# # Activar para OpenClaw (<<<CODE0>>)

- Escreva o plist para um arquivo temporário primeiro, em seguida, instalá-lo atomicamente como root:

```bash
cat <<'EOF' >/tmp/bot.molt.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>DEFAULT-OPTIONS</key>
    <dict>
        <key>Enable-Private-Data</key>
        <true/>
    </dict>
</dict>
</plist>
EOF
sudo install -m 644 -o root -g wheel /tmp/bot.molt.plist /Library/Preferences/Logging/Subsystems/bot.molt.plist
```

- Nenhuma reinicialização é necessária; logd nota o arquivo rapidamente, mas apenas novas linhas de log incluirão cargas privadas.
- Ver o resultado mais rico com o helper existente, por exemplo <<CODE0>>.

# # Desactivar após depuração

- Remova o comando: <<CODE0>>>.
- Opcionalmente, execute <<CODE1> para forçar o logd a largar o comando imediatamente.
- Lembre-se que esta superfície pode incluir números de telefone e corpos de mensagens; manter a plist no lugar apenas enquanto você precisa ativamente o detalhe extra.
