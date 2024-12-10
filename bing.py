import re
import os
import random
import requests
import time
from urllib.parse import quote
from . import ultroid_cmd, eor

BING_URL = "https://www.bing.com"

def sleep(ms):
    time.sleep(ms / 1000)

def generate_random_ip():
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))

def generate_random_user_agent():
    android_versions = ['4.0.3', '4.1.1', '4.2.2', '4.3', '4.4', '5.0.2', '5.1', '6.0', '7.0', '8.0', '9.0', '10.0', '11.0']
    device_models = ['M2004J19C', 'S2020X3', 'Xiaomi4S', 'RedmiNote9', 'SamsungS21', 'GooglePixel5']
    build_versions = ['RP1A.200720.011', 'RP1A.210505.003', 'RP1A.210812.016', 'QKQ1.200114.002', 'RQ2A.210505.003']
    selected_model = random.choice(device_models)
    selected_build = random.choice(build_versions)
    chrome_version = f"Chrome/{random.randint(1, 80)}.{random.randint(1, 999)}.{random.randint(1, 9999)}"
    user_agent = f"Mozilla/5.0 (Linux; Android {random.choice(android_versions)}; {selected_model} Build/{selected_build}) AppleWebKit/537.36 (KHTML, like Gecko) {chrome_version} Mobile Safari/537.36"
    return user_agent

class BingImageCreator:
    HEADERS = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "max-age=0",
        "content-type": "application/x-www-form-urlencoded",
        "referrer": "https://www.bing.com/images/create/",
        "origin": "https://www.bing.com",
        "user-agent": generate_random_user_agent(),
        "x-forwarded-for": generate_random_ip()
    }

    def __init__(self, cookie):
        self._cookie = f"_U={cookie}"
        if not self._cookie:
            raise ValueError("Bing cookie is required")

    def fetch_redirect_url(self, url, form_data):
        response = requests.post(url, headers={**self.HEADERS, "cookie": self._cookie}, data=form_data, allow_redirects=False)
        if not response.ok:
            raise Exception(f"Request failed\n {response.status_code}\n {response.json()}")
        redirect_url = response.headers['Location'].replace("&nfy=1", "")
        request_id = redirect_url.split("id=")[1]
        return redirect_url, request_id

    def fetch_result(self, encoded_prompt, redirect_url, request_id):
        url = f"{BING_URL}{redirect_url}"
        try:
            requests.get(url, headers={**self.HEADERS, "cookie": self._cookie})
        except Exception as e:
            raise Exception(f"Request redirect_url failed: {e}")
        get_result_url = f"{BING_URL}/images/create/async/results/{request_id}?q={encoded_prompt}"
        start_wait = time.time()
        while True:
            if time.time() - start_wait > 800:
                raise Exception("Timeout")
            sleep(1000)
            result = self.get_results(get_result_url)
            if result:
                break
        return self.parse_result(result)

    def get_results(self, get_result_url):
        response = requests.get(get_result_url, headers={**self.HEADERS, "cookie": self._cookie})
        if response.status_code != 200:
            raise Exception("Bad status code")
        content = response.text
        if not content or "errorMessage" in content:
            return None
        return content

    def parse_result(self, result):
        matches = [match.split("?w=")[0] for match in re.findall(r'src="([^"]*)"', result)]
        safe_image_links = [link for link in matches if not re.search(r'r.bing.com/rp', link)]
        unique_image_links = list(set(safe_image_links))
        filtered_image_links = [link for link in unique_image_links if not link.endswith(".svg")]
        if not filtered_image_links:
            raise Exception("No images found")
        return filtered_image_links

    def create_image(self, prompt):
        encoded_prompt = quote(prompt)
        form_data = {"q": encoded_prompt, "qa": "ds"}
        try:
            redirect_url, request_id = self.fetch_redirect_url(f"{BING_URL}/images/create?q={encoded_prompt}&rt=8&FORM=GENCRE", form_data)
            return self.fetch_result(encoded_prompt, redirect_url, request_id)
        except Exception as e:
            print("Retrying once...")
            redirect_url, request_id = self.fetch_redirect_url(f"{BING_URL}/images/create?q={encoded_prompt}&rt=8&FORM=GENCRE", form_data)
            return self.fetch_result(encoded_prompt, redirect_url, request_id)

@ultroid_cmd(pattern="bing ?(.*)")
async def generate_bing_image(event):
    if event.reply_to_msg_id:
        reply = await event.get_reply_message()
        prompt = reply.text
    else:
        prompt = event.pattern_match.group(1)
    if not prompt:
        await eor(event, "Please provide a prompt for the image generation.")
        return
    
    msg = await eor(event, "Generating image, please wait...")

    # Set up the Bing Image Creator with your cookie
    cookie = "_UR=QS=0&TQS=0&Pn=0; _HPVN=CS=eyJQbiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiUCJ9LCJTYyI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiSCJ9LCJReiI6eyJDbiI6MSwiU3QiOjAsIlFzIjowLCJQcm9kIjoiVCJ9LCJBcCI6dHJ1ZSwiTXV0ZSI6dHJ1ZSwiTGFkIjoiMjAyNC0xMC0zMVQwMDowMDowMFoiLCJJb3RkIjowLCJHd2IiOjAsIlRucyI6MCwiRGZ0IjpudWxsLCJNdnMiOjAsIkZsdCI6MCwiSW1wIjoyLCJUb2JuIjowfQ==; _clck=uqtisg%7C2%7Cfqh%7C0%7C1765; CSRFCookie=139917c5-cbe0-464a-a883-5e84ba7c20d6; _EDGE_S=SID=191CEAE27BF063B700A8FFCB7A1762CD; ANON=A=81D5F808F4DDC8BB61634B8BFFFFFFFF&E=1e6d&W=1; NAP=V=1.9&E=1e13&C=YOKF2U4GNTu_qSo-6NkgTcvsGO-kEog8w0movTeiq2sgnozzAzKCTQ&W=1; PPLState=1; KievRPSSecAuth=FACKBBRaTOJILtFsMkpLVWSG6AN6C/svRwNmAAAEgAAACLR2a/MINfJ5SARrVt+SJ5RqR8CmcBxjoos6Vloldutl/UOYQ/nFyFsJVFC2Tx4XhB90000KKA8AQX08DLBJWnQFXPc95B/3yuQkD7pbx7zua6hsmhlOmfHa0vpfzYZ8IC9/4LeEW8JFKAz5bcsp4N8BQIGSMyi/Gy7iM6VOcuC3e6VaCBKO1btUwP/oz34nU6bDUF6iARcQSLiLJAX/7+VWg2MRq4uxutN1mLvzZPSU0Lg7GL39Im21beR9jV4BnJvcpn7ekAmSnYe9I0DPMWiOzmvJ89Ve7S5K82a4FCaViHKjkN1jT7UpeuvqVtbx0d5R5gU/5Dks4QJhHe8wCzcDhh0nDQD2PLr/h3JasYEC0+MrdYOFKV7EUoi7iNm148NfmRwHu6m92XyCTVL6ovvYkSBiL9jEIdiSFUhplixmw6kXKtJmpuyXAhkSvr73+ibuGLdM3ipKOQzsiLrxwsfMd/mn3432GnD9vAVrupwoVMv7DZbkO/N5xEPyd3cB4ilVsGPT1FMXr55vIVlP5OhwM7cnwxzSM06cbnLbsaK4bJ8eUoDM23ePA/GWJxhy8pog4WxE7ai96BgX/WNRrOupUqL0I9occCOgMpnMrj9ZQ5TiSmlyJ1tOozT6jJZIVKsWR+z36Aj0RX0wk+NTCWp48MTVrnNsN8Az5AoT29s4YXLGXnRVN4QdgoJjUAkzifpIdFrIuCLgBDwX5/Dmwd3lHHKqW0C4Qnz8SYx2PEjY+uIGt2AX3+HcWNaHJAa37DkrVnQT/xzQY6WdAjTn5xUVQULYlxLK4OrG7gIs0fScBuejKkfaaQiNJC7vdM2I8EfAv2p/g+RXkCyAKeyrjHT7lsAgu26ZLRUc2bpQOby/btTEe9LsqyXMSPawytxfcMeY+PAs3ienFTjuJudBhqrCUevU+fXUrBXYnZijcrysMgAx6CQSQVTlG/mDndRa82bhCwozYPDaObIsFo88VxzTlOuDkOgtxW5PNKnCWoqjbFSfB1qsECD/Jrh0UBqCosyB4prr99SiHwoZ1pa6ktobzsMv4fB2OQos08huLxJhjD+YyRKwCEM+9Un/YRW5nZtgrV0XBx/jS4Y07G//OLrgioKD1XhMOGBxhIJS+J+bz/pz7657UkEy3N0O8NsgSb6e1nwdnFvp4Rvwu39putteiBoIk7eEpYLH51KQMsTOVbmPofHv4ulLf/QykG5w52pgYcOSoQJwkD8cxphsybVK1n21RfkQ6Sm433GlHVpw0rX6gSUldL7n+8+y77iOsTs3IiYe2BRl4oaXMmdPEdlJ88dPKtKBcyY5GWiJOvyDwaLKWO0taYC3g5uMG/5jt7Gk6GJIcrqnK0os06jepSNoXXHbICicSCODxbU/TW53qxOc3Hq/lXvElah1qn0byH75f0FhcKS1tXKFrjZzbaz4S3UlvSLfwn+CU3y5qmtvVwd2Iukfj2J6oSMzBhmNk4JNFAD+eajBhSe663JRjoF7e+233vTNeg==; _U=1oFfIxqnO5X1DoYxy8zg74-r90-tFknVxewRvQQH7Wp_ovW3Rvc0mCM9SDb8K9bKUgIumVQLng3pm_O_X6-Zhu0oc3--56fq1vdzltIbz-2XU7VWjyFe7jwQYdBCiOPgZks3Vk2fllGjEC-JBcfeZ4t3-OsIJUcdfeLTHsu4zcJjHaJvCteon_lQGVbbJ6qZdJBhJP7ppEuyC4WxQvdPVDhPgnu6L9RjzFAnrSZ_dZcg; WLS=C=877a034cbd87f65f&N=Kailash; WLID=z1EHYjEEhwNekQK5JAVdgyEsnA6k6gVCG0rmym7X6NXmWSlxf6GxFxDbf4bcO+dHx2kmB7npCME3T6NyjKlOo6z6pAaEBFeryDVnexi7auU=; SRCHUSR=DOB=20241031&TPC=1730352360000&POEX=W&T=1730352478000; _Rwho=u=d&ts=2024-10-31; SnrOvr=X=rebateson; MMCASM=ID=D8333335F0AA42E0A9CD1F6DA4A83759; SRCHHPGUSR=SRCHLANG=en&IG=B9AA13F8984144BBA72B6A1633D1F428&DM=0&BRW=HTP&BRH=T&CW=892&CH=1686&SCW=891&SCH=1686&DPR=1.9&UTC=330&PV=10.0.0; _SS=SID=16B1A599DD346A880CB5B0B0DCB26B64&R=111&RB=111&GB=0&RG=0&RP=111; _RwBf=r=1&mta=0&rc=111&rb=111&gb=0&rg=0&pc=111&mtu=0&rbb=0.0&g=0&cid=&clo=0&v=2&l=2024-10-30T07:00:00.0000000Z&lft=0001-01-01T00:00:00.0000000&aof=0&ard=0001-01-01T00:00:00.0000000&rwdbt=-62135539200&rwflt=-62135539200&rwaul2=0&o=0&p=EDGEMMXAPPACQ201903&c=MY016C&t=2006&s=2023-04-07T11:24:28.1523872+00:00&ts=2024-10-31T05:28:27.3122910+00:00&rwred=0&wls=2&wlb=0&wle=0&ccp=2&cpt=0&lka=0&lkt=0&aad=0&TH=&e=M9X4kyJjR7URYBA5NJO3oGXSePPKoX9o7bI9H1U_fENwQQ35qGAiQO7TmzhvFok2LPCy02TcmxLUfTtd8eketj6Mgjp7tY08_Kf3Ywk8yYc&A=81D5F808F4DDC8BB61634B8BFFFFFFFF; GI_FRE_COOKIE=gi_prompt=4; _clsk=138n926%7C1730352523673%7C5%7C0%7Cq.clarity.ms%2Fcollect; _C_ETH=1"
    bing_image_creator = BingImageCreator(cookie)
    try:
        image_file = bing_image_creator.create_image(prompt)
        if image_file:
            # Collect the first 4 image URLs
            images_url = image_file[:4]
        try:
            image_files = []
            for idx, img_url in enumerate(image_file):
                img_data = requests.get(img_url).content
                file_name = f"Bing_Img_{idx}.png"
                with open(file_name, "wb") as img_file:
                    img_file.write(img_data)
                image_files.append(file_name)
            # Create the caption with clickable source links
            caption = (
                f"<b>🖼️ Generated Images</b>\n\n"
                f"<b>🌟 Query:</b> <code>{prompt}</code>\n\n"
                + "<b> Image Urls:</b>"
                + " ".join([f"<a href='{url}'>{i+1}</a>" for i, url in enumerate(images_url)])
                + "\n\n<blockquote>©️ @RemainsAlways</blockquote>"
            )

            # Send all images as a single group
            await event.client.send_file(
                event.chat_id,
                file=image_files,
                caption=caption,
                parse_mode="html",
                reply_to=event.reply_to_msg_id or event.id
            )
            await msg.delete()
        finally:
            for file in image_files:
                if os.path.exists(file):
                    os.remove(file)
    except Exception as e:
        await eor(event, f"**Error:** {str(e)}")