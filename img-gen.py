import openai
openai.api_key ='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'


openai.Image.create(
  prompt="A wrestler as a cat",
  n=2,
  size="1024x1024"
)