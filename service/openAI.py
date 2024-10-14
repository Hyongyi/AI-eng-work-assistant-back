import os
from groq import Groq
import config as config



# Groq 클라이언트 초기화
client = Groq(
    api_key=config.API_KEY
)



# Prompt 템플릿을 변수로 정의
correct_grammar_template = "당신은 영어 선생님으로 당신의 직무는 영어를 배우는 학생들을 가르치고 올바른 영어를 사용할 수 있게 도와주는 선생님입니다. 학생들은 한국인이기에 무조건 한국말을 사용해야 합니다. 한국어 외에 다른 언어로 설명하면 한국 학생들은 더이상 수업에 나오지 않을 겁니다. 다른 언어를 사용하지 않도록 주의하세요. 단, 학생이 제시한 문장은 영어 그대로 사용해주세요. 학생이 문장 혹은 문단을 제시하면 검수를 한 뒤, 틀린 문법이 있을시, 문법적으로 맞게 고치고 어디가 어떻게 틀렸는지 한국어로 설명해야 합니다. 다음은 학생이 당신에게 검수를 요청하는 내용입니다.\n {sentence} \n 다음 내용을 검수하고 틀린 부분이 있으면 문법 위주로 친절하게 단계별로 설명해주세요. "


description_template = "당신은 영어 선생님으로 당신의 직무는 영어를 배우는 학생들을 가르치고 올바른 영어를 사용할 수 있게 도와주는 선생님입니다. 학생들은 한국인이기에 무조건 한국말을 사용해야 합니다. 한국어 외에 다른 언어로 설명하면 한국 학생들은 더이상 수업에 나오지 않을 겁니다. 다른 언어를 사용하지 않도록 주의하세요. 단, 학생이 제시한 문장은 영어 그대로 사용해주세요. 학생이 영어로 된 문장 혹은 문단을 제시하면 당신은 이 문장을 분석해서 요약하여 설명해주어야 합니다. 간결하게 설명하되, 내용이 누락되면 안됩니다. 다음은 학생이 당신에게 물어보는 내용입니다.\n {sentence} \n 다음 내용을 분석한 뒤, 한국어로 요약하여 전달해주세요. 문장은 끊어지지 않고 전체적으로 이어지게 만들어주세요."




def call_Groq_api(prompt):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=config.LLM_MODEL,
    )
    
    
    return response.choices[0].message.content

def prompt_format(prompt, sentence):
    prompt_template = prompt.format(sentence=sentence)
    return call_Groq_api(prompt_template)


print(prompt_format(correct_grammar_template, "i name is Austin. What are your name?"))
print(prompt_format(description_template, "In the modern world, the importance of technology cannot be overstated, as it has transformed every aspect of our daily lives, from how we communicate and socialize to how we work and learn. The advent of the internet has connected people across the globe, allowing for instantaneous communication and the sharing of information on an unprecedented scale. This connectivity has not only fostered the growth of social media platforms, enabling individuals to maintain relationships regardless of geographical boundaries, but it has also facilitated the rise of remote work and online education, giving people the flexibility to work or study from anywhere in the world. Moreover, advancements in artificial intelligence and machine learning are revolutionizing industries by automating tasks, enhancing efficiency, and providing valuable insights through data analysis. However, this rapid technological evolution also brings challenges, such as concerns over privacy, the digital divide, and the impact of automation on employment. As we continue to navigate this complex landscape, it is crucial to strike a balance between leveraging the benefits of technology and addressing the ethical implications it presents, ensuring that progress serves the greater good while fostering inclusivity and sustainability."))
