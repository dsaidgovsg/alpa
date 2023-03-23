import time
import numpy as np
import requests
import argparse

test_prompts = [
    "Computer science is the study of computation and",
    "Ion Stoica is a Romanian-American computer scientist specializing in",
    "The University of California, Berkeley is a public",
    "Today is a good day and I want to", "What is the valuation of Databricks?",
    "Paris is the capital city of", "Which country has the most population?",
    "What do you think about the future of Cryptocurrency?",
    "What do you think about the meaning of life?",
    "Donald Trump is the president of",
    "GPT-3 is a large language model that is capable of"
]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n-warmup", type=int, default=0)
    parser.add_argument("--max-length", type=int, default=256)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()

    # Do some param check
    n_warmup = args.n_warmup
    max_length = args.max_length

    decode_speeds = []

    for i in range(len(test_prompts)):
        prompt = test_prompts[i]

        pload = {
            "model": "default",
            "prompt": prompt,
            "max_tokens": max_length,
            "temperature": 0.7,
            "top_p": 0.7,
        }

        # Warm up
        for _ in range(n_warmup):
            res = requests.post(url="https://llama.govtext.gov.sg:20001/completions", json=pload, timeout=120)
            output = res.json()

        # Benchmark a prompt
        tic = time.time()
        t1 = time.time()
        res = requests.post(url="https://llama.govtext.gov.sg:20001/completions", json=pload, timeout=120)
        print(f"t1: {time.time() - t1}")
        output = res.json()
        latency = time.time() - tic
        generated_string = output["choices"][0]["text"]
        speed = len(generated_string) / latency
        decode_speeds.append(speed)

        print(
            f"input length: {len(prompt)}, output_length: {len(generated_string)}, "
            f"speed: {speed:.2f} words/s", f"output: {generated_string}"
        )

    avg_speed = np.mean(decode_speeds)        
    print(f"average speed: {avg_speed:.2f} words/s")
