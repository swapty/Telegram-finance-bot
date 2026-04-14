# Deployment Guide

## Quick Deploy Options

### Option 1: Railway.app (Recommended)

1. **Create account** at railway.app
2. **New Project** → Deploy from GitHub
3. **Add environment variables**:
   ```
   BOT_TOKEN=your_token
   ADMIN_ID=your_id
   DATABASE_PATH=/data/bot.db
   ```
4. **Add volume** for persistent database:
   - Mount path: `/data`
   - Size: 1GB
5. **Deploy** - Railway will auto-detect Python and install dependencies

### Option 2: Render.com

1. **Create account** at render.com
2. **New** → Background Worker
3. **Connect repository**
4. **Build Command**: `pip install -r requirements.txt`
5. **Start Command**: `python app/main.py`
6. **Environment Variables**:
   ```
   BOT_TOKEN=your_token
   ADMIN_ID=your_id
   DATABASE_PATH=/var/data/bot.db
   ```
7. **Add Disk**:
   - Name: `data`
   - Mount path: `/var/data`
   - Size: 1GB

### Option 3: Fly.io

1. **Install flyctl**: `curl -L https://fly.io/install.sh | sh`
2. **Login**: `flyctl auth login`
3. **Create fly.toml**:
   ```toml
   app = "your-bot-name"
   primary_region = "iad"

   [build]
     builder = "paketobuildpacks/builder:base"

   [[services]]
     internal_port = 8080
     protocol = "tcp"

   [mounts]
     source = "bot_data"
     destination = "/data"
   ```
4. **Set secrets**:
   ```bash
   flyctl secrets set BOT_TOKEN=your_token
   flyctl secrets set ADMIN_ID=your_id
   ```
5. **Deploy**: `flyctl deploy`

### Option 4: VPS (DigitalOcean, Linode, etc.)

1. **Create Ubuntu server** (20.04 or 22.04)
2. **SSH into server**
3. **Install Python**:
   ```bash
   sudo apt update
   sudo apt install python3.11 python3.11-venv python3-pip git
   ```
4. **Clone repository**:
   ```bash
   git clone your-repo-url
   cd your-repo
   ```
5. **Create virtual environment**:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
6. **Set up environment**:
   ```bash
   cp .env.example .env
   nano .env  # Edit with your values
   ```
7. **Create systemd service** (`/etc/systemd/system/finbot.service`):
   ```ini
   [Unit]
   Description=Financial News Bot
   After=network.target

   [Service]
   Type=simple
   User=your-user
   WorkingDirectory=/home/your-user/your-repo
   Environment="PATH=/home/your-user/your-repo/venv/bin"
   ExecStart=/home/your-user/your-repo/venv/bin/python app/main.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
8. **Enable and start**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable finbot
   sudo systemctl start finbot
   sudo systemctl status finbot
   ```

## Post-Deployment

### 1. Test the Bot
- Send `/start` to your bot
- Complete the setup flow
- Verify language selection works
- Check settings save correctly

### 2. Create Initial Promo Codes
```bash
python admin.py create-promo LAUNCH2024 1
python admin.py create-promo BETA100 12
```

### 3. Monitor Logs
- Railway: Check logs in dashboard
- Render: View logs in UI
- Fly.io: `flyctl logs`
- VPS: `sudo journalctl -u finbot -f`

### 4. Test News Delivery
Wait for the scheduled job to run, or manually trigger by:
- Instant: Wait 15 minutes
- Daily: Set time in config and restart
- Weekly: Set day/time and restart

## Monitoring

### Check Bot Status
```bash
python admin.py stats
```

### Check Database
```bash
sqlite3 bot.db
.tables
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM sent_news;
.exit
```

## Scaling Considerations

### When to Scale
- 100+ users: Current setup fine
- 1,000+ users: Consider PostgreSQL
- 10,000+ users: Add caching, queue system

### Database Migration (SQLite → PostgreSQL)
1. Install PostgreSQL adapter: `pip install asyncpg`
2. Update `config.py` with PostgreSQL connection
3. Modify `db.py` to use asyncpg instead of aiosqlite
4. Export/import data

## Troubleshooting

### Bot Not Responding
- Check `BOT_TOKEN` is correct
- Verify bot is running: check logs
- Test network connectivity

### News Not Sending
- Check scheduler is started
- Verify RSS feeds are accessible
- Check user has active subscription
- Review logs for errors

### Database Locked
- Ensure only one bot instance running
- Check file permissions on database
- Restart bot service

## Backup Strategy

### Automatic Backups
```bash
# Add to crontab
0 2 * * * cp /path/to/bot.db /path/to/backups/bot-$(date +\%Y\%m\%d).db
```

### Manual Backup
```bash
cp bot.db bot-backup-$(date +%Y%m%d-%H%M%S).db
```

## Security Checklist

- [ ] Environment variables not committed to git
- [ ] Database file has proper permissions (600)
- [ ] Bot token kept secret
- [ ] Admin ID verified
- [ ] HTTPS used for webhooks (if applicable)
- [ ] Regular backups configured
- [ ] Logs reviewed periodically

## Performance Tips

1. **Optimize News Fetching**: Cache RSS feeds for 5-10 minutes
2. **Batch Database Writes**: Group multiple updates
3. **Rate Limiting**: Add delays between messages
4. **Resource Limits**: Set max news items per batch
5. **Clean Old Data**: Archive old sent_news entries

## Support

For deployment issues:
1. Check logs first
2. Review this guide
3. Contact admin
4. Open GitHub issue
