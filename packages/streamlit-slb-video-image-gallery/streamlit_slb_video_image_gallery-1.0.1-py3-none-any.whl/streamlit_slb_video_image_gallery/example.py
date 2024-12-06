import os
import base64
import streamlit as st
import gzip
import json
from datetime import date, datetime
from typing import List
from PIL import Image
import io

from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import OAuthInteractive, OAuthClientCredentials
from streamlit_slb_video_image_gallery import streamlit_slb_video_image_gallery

from models.viewer_data import ViewerData
from models.deck import Deck
from models.beacon import Beacon
from models.camera import Camera
from models.coordinate import Coordinate
from pandas import DataFrame
from helpers.cognite_helper import get_deck_list

import time


def assign_auth(project_name):

    if project_name == "slb-test":
        tenant_id = os.environ.get("CDF_SLBTEST_TENANT_ID")
        client_id = os.environ.get("CDF_SLBTEST_CLIENT_ID")
        client_secret = os.environ.get("CDF_SLBTEST_CLIENT_SECRET")
        cluster = os.environ.get("CDF_SLBTEST_CLUSTER")
    elif project_name == "petronas-pma-dev" or project_name == "petronas-pma-playground":
        tenant_id = os.environ.get("CDF_PETRONASPMA_TENANT_ID")
        cluster = os.environ.get("CDF_PETRONASPMA_CLUSTER")
        client_id = os.environ.get("CDF_PETRONASPMA_CLIENT_ID")
        client_secret = ""
    elif project_name == "hess-malaysia-dev":
        tenant_id = os.environ.get("CDF_HESSDEV_TENANT_ID")
        client_id = os.environ.get("CDF_HESSDEV_CLIENT_ID")
        client_secret = os.environ.get("CDF_HESSDEV_CLIENT_SECRET")
        cluster = os.environ.get("CDF_HESSDEV_CLUSTER")
    elif project_name == "hess-malaysia-prod":
        tenant_id = os.environ.get("CDF_HESSPROD_TENANT_ID")
        client_id = os.environ.get("CDF_HESSPROD_CLIENT_ID")
        client_secret = os.environ.get("CDF_HESSPROD_CLIENT_SECRET")
        cluster = os.environ.get("CDF_HESSPROD_CLUSTER")
    elif project_name == "mubadala-dev":
        # tenant_id = os.environ.get("CDF_MUBADALADEV_TENANT_ID")
        # cluster = os.environ.get("CDF_MUBADALADEV_CLUSTER")
        # client_id = os.environ.get("CDF_MUBADALADEV_CLIENT_ID")
        # client_secret = os.environ.get("CDF_MUBADALADEV_CLIENT_SECRET")
        tenant_id = '6e302fe9-1186-4281-9fb3-944d7bb828cc'
        cluster = 'az-sin-sp-001'
        client_id = '33fbccca-1f13-4339-9d46-641822badbfe'
        client_secret = 'p878Q~xF6VKi2M7QK_wXO4uwIThmWc1~R~fcJb9E'

    base_url = f"https://{cluster}.cognitedata.com"
    scopes = [f"{base_url}/.default"]

    return {
        "tenant_id": tenant_id,
        "client_id": client_id,
        "client_secret": client_secret,
        "cluster": cluster,
        "base_url": base_url,
        "project_name": project_name,
        "scopes": scopes
    }


def interactive_client(project_name):

    auth_data: any = assign_auth(project_name)

    """Function to instantiate the CogniteClient, using the interactive auth flow"""
    return CogniteClient(
        ClientConfig(
            client_name=auth_data['project_name'],
            project=auth_data['project_name'],
            base_url=auth_data['base_url'],
            credentials=OAuthInteractive(
                authority_url=f"https://login.microsoftonline.com/{auth_data['tenant_id']}",
                client_id=auth_data['client_id'],
                scopes=auth_data['scopes'],
            ),
        )
    )


def client_credentials(project_name):

    auth_data = assign_auth(project_name)

    credentials = OAuthClientCredentials(
        token_url=f"https://login.microsoftonline.com/{auth_data['tenant_id']}/oauth2/v2.0/token",
        client_id=auth_data['client_id'],
        client_secret=auth_data['client_secret'],
        scopes=auth_data['scopes']
    )

    config = ClientConfig(
        client_name=auth_data['project_name'],
        project=auth_data['project_name'],
        base_url=auth_data['base_url'],
        credentials=credentials,
    )
    client = CogniteClient(config)

    return client


def connect(project_name):
    auth = assign_auth(project_name=project_name)
    if auth["client_secret"] == "":
        return interactive_client(project_name)
    else:
        return client_credentials(project_name)


st.set_page_config(layout='wide')
st.subheader("Streamlit Slb Image and Video Gallery")

client: CogniteClient = connect("mubadala-dev")

selected_deck_external_id: int = None
selected_deck_image_id: int = None
imagelist_df: DataFrame = None
viewer_data: ViewerData = None
data_3d = None


def render_selectbox() -> int:
    deckData = get_deck_list(client=client)
    options = {item["name"]: item["externalId"]
               for item in deckData["listDeck"]["items"]}
    deck_name = st.selectbox(label="Select Deck", options=options.keys())
    selected_deck_external_id = options[deck_name]
    return selected_deck_external_id


def get_image_from_id(image_id) -> str:
    image_bytes = client.files.download_bytes(id=image_id)
    base64_str = base64.b64encode(image_bytes).decode("utf-8")
    return base64_str


def get_files_metadata(source):
    file_list = client.files.list(source=source, limit=-1)
    return file_list


def parse_date(time_string):
    for fmt in ["%m/%d/%Y %H:%M:%S", "%m/%d/%Y %H:%M"]:
        try:
            return datetime.strptime(time_string, fmt).date()
        except ValueError:
            continue
    raise ValueError(
        f"Time data '{time_string}' does not match any supported format")


def check_files_within_date_range():
    # start = datetime.strptime("09/30/2024", "%m/%d/%Y").date()
    start = date(2024, 9, 1)
    end = date(2024, 9, 30)
    # st.write(st.session_state)
    # end = datetime.strptime("09/01/2024", "%m/%d/%Y").date()
    files_within_date_range = []
    temp = []
    file_metadata = get_files_metadata("agora")
    print(len(file_metadata), 'file metadata len')
    # st.write(len(file_metadata), 'file metadata len')
    temp_item = []
    for item in file_metadata:
        temp_item.append(item)
        if item.metadata != None:
            # image_date = datetime.strptime(item.metadata["alert_time"], "%m/%d/%Y %H:%M").date()
            image_date = parse_date(item.metadata["alert_time"])
            temp.append(image_date)
            if start <= image_date <= end:
                # st.text
                files_within_date_range.append(item)
    # print(temp[0])
    # print(files_within_date_range[0])
    return files_within_date_range


# selected_deck_external_id = render_selectbox()
# col1, col2 = st.columns(2)

# with col1:
#     threed_container = st.empty()
# with col2:
#     data_container = st.empty()

def get_image_vid(file_data):

    # Total number of API requests
    # total_requests = len(external_id_list)
    images = []
    start = time.time()

    for i, data in enumerate(file_data):
        temp = client.files.download_bytes(external_id=data.external_id)
        # (len(temp), 'before_compress')

        pil_image = Image.open(io.BytesIO(temp))
        optimized_image = io.BytesIO()
        pil_image.save(optimized_image, format="JPEG",
                       quality=50)  # Adjust quality (1-100)
        optimized_image.seek(0)
        compressed_bytes = optimized_image.getvalue()

        # print(f"Compressed size: {len(compressed_bytes)} bytes")

        # base64_image = base64.b64encode(temp).decode('utf-8')
        base64_image = base64.b64encode(compressed_bytes).decode('utf-8')
        images.append(
            {'image': base64_image, 'id': data.external_id, **data.metadata, 'alert_type2': data.metadata['alert_type'].strip().replace(" ", "").strip("{'}")})
    # print(images[0])
    end = time.time()

    print(f"{end-start} elapse time")
    # return images
    return images


@st.fragment()
def render_viewer():
    global viewer_data
    global data_3d
    temp = check_files_within_date_range()

    # deck_image_str = get_image_from_id(selected_deck_image_id)
    # with threed_container:
    # print(data[0])
    # print(len(temp))
    data_3d = 1
    num_of_images_per_page = 10

    start_idx = (data_3d - 1) * num_of_images_per_page
    end_idx = start_idx + num_of_images_per_page

    # data = get_image_vid(temp[start_idx:end_idx])
    # data = get_image_vid(temp)
    data_3d = streamlit_slb_video_image_gallery(
        height=1000, deck_image='', enable_animation=False, data=[], dataLength=0)

    # st.write("This many: %s" % data_3d)
    # show_3d_data()


@st.fragment()
def show_3d_data():
    # data_container.empty()
    # with data_container:
    #     if data_3d is not None:
    #         st.write(data_3d)
    # data_container.empty()
    # with st.container(height=900):
    #     if data_3d is not None:
    #         st.write(data_3d)
    pass


# viewer_data = get_data()
render_viewer()
