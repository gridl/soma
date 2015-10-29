from optparse import OptionParser
from collections import namedtuple

# Options holds the command line options
Options = namedtuple("Options", "KafkaHost KafkaTopic")

# Parses the command line options
def parse_commandline():
    parser = OptionParser(usage='%prog [options] <Excel File>')

    parser.add_option('-k', '--kafka-host',
                      dest="kafka_host",
                      default="localhost:9092",
                      help="Hostname (and port) of the Kafka data backbone server."
                      )

    parser.add_option('-t', '--kafka-topic',
                      dest="kafka_topic",
                      default="soma",
                      help="The topic name under which messages are broadcasted to Kafka."
                      )

    options, remainder = parser.parse_args()

    # if len(remainder) != 1:
    #     parser.print_help()
    #     raise Exception("Wrong numer of arguments")

    return Options(
        KafkaHost=options.kafka_host,
        KafkaTopic=options.kafka_topic
    )
