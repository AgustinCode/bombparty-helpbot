from driver import JKLMBot

if __name__ == "__main__":
    try:
        bot = JKLMBot("CDRD")
        bot.run()
    except Exception as e:
        print(f"There was an error when executing the script: {e}")
    finally:
        if bot.driver:
            bot.driver.quit()