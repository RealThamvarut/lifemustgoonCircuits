from read_card import RC522CardReader
try:
  while True:
    #rdr.wait_for_tag()
    card_reader = RC522CardReader()
    uid = card_reader.read_with_debounce()
    if uid is not None:
        print("UID: " + card_reader.translate_uid(uid))
    

except KeyboardInterrupt:
  # Graceful shutdown
  card_reader.cleanup()