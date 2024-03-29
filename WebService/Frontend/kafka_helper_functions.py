from confluent_kafka import Producer, Consumer, KafkaError
import streamlit as st
from trigger_dag import trigger_dag
import os
# Kafka cluster configuration
topic = 's3'
security_protocol='SASL_SSL'
sasl_mechanisms='PLAIN'
sasl_username=os.getenv('sasl_username')
sasl_password=os.getenv('sasl_password')
bootstrap_servers = os.getenv('bootstrap_servers')
def produce_message(message, topic='s3'):
    
    producer_config = {
        'bootstrap.servers': bootstrap_servers,
        'security.protocol': security_protocol,
        'sasl.mechanisms': sasl_mechanisms,
        'sasl.username': sasl_username,
        'sasl.password':sasl_password
    }
    
    producer = Producer(producer_config)
    
    try:
        # Produce message to Kafka topic
        producer.produce(topic, message.encode('utf-8'))
        producer.flush()  # Wait for message to be sent
        print(f"Message '{message}' produced successfully to topic '{topic}'")
    except Exception as e:
        print(f"Failed to produce message: {e}")
    finally:
        producer.flush()  # Flush and close producer

def consume_message(topic='s3'):
    consumer_config = {
        'bootstrap.servers': bootstrap_servers,
         'security.protocol': security_protocol,
        'sasl.mechanisms': sasl_mechanisms,
        'sasl.username': sasl_username,
        'sasl.password':sasl_password,
        'group.id': 'python-group-1',
        'auto.offset.reset': 'earliest'
    }
    
    consumer = Consumer(consumer_config)
    
    # Subscribe to Kafka topic
    consumer.subscribe([topic])
    
    try:
        while True:
            # Poll for new messages
            message = consumer.poll(timeout=1.0)
            
            if message is None:
                continue
            if message.error():
                if message.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition, ignore
                    st.write('partition error')
                    continue
                else:
                    st.write("stopping")
                    print(f"Consumer error: {message.error()}")
                    break
            s3_uri = message.value().decode('utf-8')
            info, run_id = trigger_dag(dag_id='bigdag',s3_uri=s3_uri)
            st.write(info)
            st.write(run_id)
            st.write(f"Consumed message: {s3_uri}")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()  # Close consumer when done
