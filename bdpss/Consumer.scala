import java.time.Duration
import java.time.temporal.ChronoUnit
import java.util.Properties

import org.apache.kafka.clients.consumer.KafkaConsumer

import scala.collection.JavaConverters._

object Consumer {

  def main(args: Array[String]): Unit = {

    // Aqui definiremos la configuracion
    val props: Properties = new Properties()
    props.put("group.id", "test")
    props.put("bootstrap.servers", "localhost:9092")
    props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer")
    props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer")

    // Declaramos el consumidor de kafca con la configuracion qu hemos definido
    val consumidor = new KafkaConsumer[String, String](props)

    // Declaramos el topic al que tiene que estar atento el consumido
    val topic = List("practica")

    try {
      consumidor.subscribe(topic.asJava)
      while (true) {
        val msg = consumidor.poll(Duration.of(1, ChronoUnit.SECONDS))
        // Aqui filtramos los menajes para eliminar los nombres elegidos
        msg.asScala
          .filter(it => !it.value().contains("Giavani") && !it.value().contains("Noell"))
          .foreach(m => println(m.value()))
      }
    } catch {
      case e: Exception => e.printStackTrace()
    } finally {
      consumidor.close()
    }


  }
}
