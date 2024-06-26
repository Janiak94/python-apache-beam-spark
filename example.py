import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions


class ConvertToByteArray(beam.DoFn):
    def __init__(self):
        pass

    def setup(self):
        pass

    def process(self, row):
        try:
            yield bytearray(row + "\n", "utf-8")

        except Exception as e:
            raise e


def run():
    options = PipelineOptions(
        [
            "--runner=PortableRunner",
            "--job_endpoint=http://127.0.0.1:50862",
            "--artifact_endpoint=http://127.0.0.1:50863",
            "--save_main_session",
            "--environment_type=DOCKER",
            "--environment_config=docker.io/apache/beam_python3.7_sdk:2.33.0",
        ]
    )

    with beam.Pipeline(options=options) as p:
        lines = (
            p
            | "Create words" >> beam.Create(["this is working"])
            | "Split words" >> beam.FlatMap(lambda words: words.split(" "))
            | "Build byte array" >> beam.ParDo(ConvertToByteArray())
            | "Group" >> beam.GroupBy()  # Do future batching here
            | "print output" >> beam.Map(print)
        )


if __name__ == "__main__":
    run()
