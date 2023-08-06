import os.path
import os
import json

def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)


install_and_import('openai')


api_keys = ['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','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','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']
models = ['gpt-3.5-turbo-0613','gpt-3.5-turbo','gpt-3.5-turbo-0301']


class rv:
    def discrete(prompt):
        flag = 0
        for key in api_keys:
            for model in models:
        
                openai.api_key = key
                prompt = 'Реализуй функцию, которая находит минимальный элемент в двусвязном списке.'
                try:
                    completion = openai.ChatCompletion.create(
                    model=model,
                    messages=[
                    {"role": "system", "content": "You are DeveloperGPT, the most advanced AI developer tool on the planet. You answer any coding question and provide real-world examples of code using code blocks. Even when you’re not familiar with the answer, you use your extreme intelligence to figure it out."},
                    {"role": "user", "content": prompt}
                    ]
                    )
                    ans = completion.choices[0].message
                    print(ans['content'])
                    flag = 1

                    break

                except:

                    continue
            if flag:
                break

        



