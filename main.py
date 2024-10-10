import disnake
from disnake.ext import commands, tasks

bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all())

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.webhook_loop_running = False  # Флаг для отслеживания состояния цикла
        self.webhook_url = "https://discord.com/api/webhooks/1286377307241582704/NUvYZk_IiYnzCdy51ZaaNilZW-VWChHY4M09ezEN1AodAAzod7-LD11Pui9jlZgIK-4N"
        self.webhook = disnake.Webhook.from_url(self.webhook_url, adapter=disnake.AsyncWebhookAdapter())

    @commands.slash_command(name='start_spam', description="Начать отправку сообщений через вебхук")
    async def start_spam(self, interaction: disnake.ApplicationCommandInteraction):
        if not self.webhook_loop_running:  # Проверяем, что цикл не запущен
            self.webhook_loop_running = True
            await interaction.response.send_message('Цикл запущен, сообщения будут отправляться через вебхук.')
            self.webhook_loop.start()  # Запуск цикла
        else:
            await interaction.response.send_message('Цикл уже запущен!')

    @commands.slash_command(name='stop_spam', description="Остановить отправку сообщений через вебхук")
    async def stop_spam(self, interaction: disnake.ApplicationCommandInteraction):
        if self.webhook_loop_running:
            self.webhook_loop_running = False
            self.webhook_loop.cancel()  # Останавливаем цикл
            await interaction.response.send_message('Цикл остановлен.')
        else:
            await interaction.response.send_message('Цикл не запущен.')

    @tasks.loop(seconds=1)  # Интервал между сообщениями
    async def webhook_loop(self):
        if self.webhook_loop_running:  # Проверка состояния цикла
            await self.webhook.send(
                "Сообщение через вебхук!", 
                username="Fuhrer 🇷🇺",  # Установка ника
                avatar_url="https://media.discordapp.net/attachments/471995793964793857/1294015163657228298/IMG_20241010_221401.jpg?ex=67097908&is=67082788&hm=b209d349251235aff42fd7129ffd6115f402d8eec55e7e6c4c040be136142ef4&=&format=webp"  # Установка аватара
            )

bot.add_cog(Test(bot))

@bot.event
async def on_ready():
    print(f"Бот запущен как {bot.user}")

bot.run("MTI5NDAyNzgyMTUwODcyNjkzOA.GP0xOf.ZGTJTijkia2XPuj2KR4-IHzHzBRBob0LN_Npkc")