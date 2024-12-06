<div align="center">

<h1>🤗🔭 Observers 🔭🤗</h1>

<h3 align="center">A Lightweight Library for AI Observability</h3>

</div>

![Observers Logo](./assets/observers.png)

## Installation

First things first! You can install the SDK with pip as follows:

```bash
pip install observers
```

Or if you want to use other LLM providers through AISuite or Litellm, you can install the SDK with pip as follows:

```bash
pip install observers[aisuite] # or observers[litellm]
```

## Usage

We differentiate between observers and stores. Observers wrap generative AI APIs (like OpenAI or llama-index) and track their interactions. Stores are classes that sync these observations to different storage backends (like DuckDB or Hugging Face datasets).

To get started you can run the code below. It sends requests to a HF serverless endpoint and log the interactions into a Hub dataset, using the default store `DatasetsStore`. The dataset will be pushed to your personal workspace (http://hf.co/{your_username}). To learn how to configure stores, go to the next section.

```python
from observers.observers import wrap_openai
from observers.stores import DuckDBStore
from openai import OpenAI

store = DuckDBStore()

openai_client = OpenAI()
client = wrap_openai(openai_client, store=store)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Tell me a joke."}],
)
```

## Observers

### Supported Observers

- [OpenAI](https://openai.com/) and every other LLM provider that implements the [OpenAI API message formate](https://platform.openai.com/docs/api-reference)
- [AISuite](https://github.com/andrewyng/aisuite), which is an LLM router by Andrew Ng and which maps to [a lot of LLM API providers](https://github.com/andrewyng/aisuite/tree/main/aisuite/providers) with a uniform interface.

### Change OpenAI compliant LLM provider

The `wrap_openai` function allows you to wrap any OpenAI compliant LLM provider. Take a look at [the example doing this for Ollama](./examples/ollama_example.py) for more details.

## Stores

### Supported Stores

| Store | Example | Annotate | Local | Free | UI filters | SQL filters |
|-------|---------|----------|-------|------|-------------|--------------|
| [Hugging Face Datasets](https://huggingface.co/docs/huggingface_hub/en/package_reference/io-management#datasets) | [example](./examples/datasets_example.py) | ❌ | ❌ | ✅ | ✅ | ✅ |
| [DuckDB](https://duckdb.org/) | [example](./examples/duckdb_example.py.py) | ❌ | ✅ | ✅ | ❌ | ✅ |
| [Argilla](https://argilla.io/) | [example](./examples/argilla_example.py) | ✅ | ❌ | ✅ | ✅ | ❌ |

### Viewing / Querying

#### Hugging Face Datasets Store

To view and query Hugging Face Datasets, you can use the [Hugging Face Datasets Viewer](https://huggingface.co/docs/hub/en/datasets-viewer). You can [find example datasets on the Hugging Face Hub](https://huggingface.co/datasets?other=observers). From within here, you can query the dataset using SQL or using your own UI. Take a look at [the example](./examples/datasets_example.py) for more details.

![Hugging Face Datasets Viewer](./assets/datasets.png)

#### DuckDB Store

The default store is [DuckDB](https://duckdb.org/) and can be viewed and queried using the [DuckDB CLI](https://duckdb.org/#quickinstall). Take a look at [the example](./examples/duckdb_example.py) for more details.

```bash
> duckdb store.db
> from openai_records limit 10;
┌──────────────────────┬──────────────────────┬──────────────────────┬──────────────────────┬───┬─────────┬──────────────────────┬───────────┐
│          id          │        model         │      timestamp       │       messages       │ … │  error  │     raw_response     │ synced_at │
│       varchar        │       varchar        │      timestamp       │ struct("role" varc…  │   │ varchar │         json         │ timestamp │
├──────────────────────┼──────────────────────┼──────────────────────┼──────────────────────┼───┼─────────┼──────────────────────┼───────────┤
│ 89cb15f1-d902-4586…  │ Qwen/Qwen2.5-Coder…  │ 2024-11-19 17:12:3…  │ [{'role': user, 'c…  │ … │         │ {"id": "", "choice…  │           │
│ 415dd081-5000-4d1a…  │ Qwen/Qwen2.5-Coder…  │ 2024-11-19 17:28:5…  │ [{'role': user, 'c…  │ … │         │ {"id": "", "choice…  │           │
│ chatcmpl-926         │ llama3.1             │ 2024-11-19 17:31:5…  │ [{'role': user, 'c…  │ … │         │ {"id": "chatcmpl-9…  │           │
├──────────────────────┴──────────────────────┴──────────────────────┴──────────────────────┴───┴─────────┴──────────────────────┴───────────┤
│ 3 rows                                                                                                                16 columns (7 shown) │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

#### Argilla Store

The Argilla Store allows you to sync your observations to [Argilla](https://argilla.io/). To use it, you first need to create a [free Argilla deployment on Hugging Face](https://docs.argilla.io/latest/getting_started/quickstart/). Take a look at [the example](./examples/argilla_example.py) for more details.

![Argilla Store](./assets/argilla.png)

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)
