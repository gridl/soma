from kafka.client   import KafkaClient
from kafka.producer import SimpleProducer
from collections    import namedtuple

KafkaWriterConfig = namedtuple("KafkaWriterConfig", "Host Topic")

class KafkaWriter:
   'Writes your data to Apache Kafka'

   def __init__(self, config):
      self._config = config
      self._kafka = None
      self._producer = None

   def connect(self):
       self._kafka =  KafkaClient(self._config.Host)
       self._producer = SimpleProducer(self._kafka)

   def write(self, message):
       self._producer.send_messages(self._config.Topic, message)
