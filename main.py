from driver import JKLMBot

if __name__ == "__main__":
    try:
        bot = JKLMBot("CDRD")
        bot.run()
    except Exception as e:
        print(f"Error durante la ejecución del script: {e}")
    finally:
        if bot.driver:
            bot.driver.quit()