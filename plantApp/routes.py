# app/routes.py
from flask import Blueprint, jsonify, request, Response, render_template
# from .extensions import db
from PIL import Image
from sqlalchemy.dialects.mssql import IMAGE

from .models import *
import io
import os
import cv2
import requests


main = Blueprint('main', __name__)

camera = cv2.VideoCapture(0)

@main.route('/stop_camera')
def stop_camera():
    global camera
    if camera is not None:
        camera.release()
        camera = None
    return "Camera stopped"
@main.route('/video_feed', methods=['POST'])
def video_feed():
    camera = cv2.VideoCapture(0)
    def generate():
        while True:
            success, frame = camera.read()
            if not success:
                break
            # Mã hóa frame thành JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # Gửi frame dưới dạng chuỗi multipart
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
@main.route('/')
def index():
    plants = Plant.query.all()
    return render_template('index.html', plants=plants)
@main.route('/shop-details')
def shop_details():
    regions_list = []
    plant_id = request.args.get('plant_id')
    plant_infor = Plant.query.filter(Plant.id == plant_id).first()
    ingredients = Ingredient.query.filter(Ingredient.plant_id == plant_id).all()
    # Lấy tất cả các region_id liên quan đến plant_id
    region_ids = (
        PlantRegion.query.filter(PlantRegion.plant_id == plant_id)
        .with_entities(PlantRegion.region_id)
        .all()
    )

    # Chuyển region_ids từ danh sách các tuple [(1,), (2,), ...] thành danh sách [1, 2, ...]
    region_ids = [region_id[0] for region_id in region_ids]

    # Lấy tất cả các tên vùng tương ứng với region_ids
    regions = Region.query.filter(Region.id.in_(region_ids)).all()

    # Tạo danh sách các tên vùng
    regions_list = [region.name for region in regions]

    documentations = Documentation.query.filter(Documentation.plant_id == plant_id).all()
    images = PlantImage.query.filter(PlantImage.plant_id == plant_id).all()
    return render_template('shop-details.html', plant_infor=plant_infor, ingredients=ingredients, regions=regions_list, documentations=documentations, images=images)

@main.route('/plant-details-app', methods = ["GET"])
def plant_details_app():
    plant_id = request.args.get('plant_id')

    if not plant_id:
        return jsonify({"error": "plant_id is required"}), 400

    # Lấy thông tin cây
    plant_infor = Plant.query.filter(Plant.id == plant_id).first()
    if not plant_infor:
        return jsonify({"error": "Plant not found"}), 404

    # Lấy danh sách nguyên liệu
    ingredients = Ingredient.query.filter(Ingredient.plant_id == plant_id).all()

    # Lấy các region liên quan đến plant_id
    region_ids = (
        PlantRegion.query.filter(PlantRegion.plant_id == plant_id)
        .with_entities(PlantRegion.region_id)
        .all()
    )
    region_ids = [region_id[0] for region_id in region_ids]
    regions = Region.query.filter(Region.id.in_(region_ids)).all()
    regions_list = [region.name for region in regions]

    # Lấy danh sách tài liệu và hình ảnh
    documentations = Documentation.query.filter(Documentation.plant_id == plant_id).all()
    images = PlantImage.query.filter(PlantImage.plant_id == plant_id).all()

    # Chuẩn bị dữ liệu JSON
    response_data = {
        "plant_info": {
            "id": plant_infor.id,
            "name": plant_infor.name,
            "scientific_name": plant_infor.scientific_name,
            "family": plant_infor.family,
            "description": plant_infor.description,
            "image_url": plant_infor.image_url,
            "uses": plant_infor.uses,
            # Thêm các thuộc tính khác của plant_infor nếu cần
        },
        "ingredients": [{"id": ingredient.id, "plant_id": ingredient.plant_id ,"name": ingredient.name} for ingredient in ingredients],
        "regions": regions_list,
        "documentations": [{"id": doc.id ,"title": doc.title, "plant_id": doc.plant_id, "url": doc.url} for doc in documentations],
        "images": [{"id": img.id, "plant_id": img.plant_id ,"url": img.url} for img in images],
    }

    # Trả về JSON response
    return jsonify(response_data), 200
# Path to the image file (you can replace this with the actual image path or upload functionality)
image_path = "D:\\pbl4\\PBL4-PlantMedicalApp\\images.jpg"

# URL of Raspberry Pi API (the receiving API)
raspberry_pi_url = "http://10.10.82.139:5001/receive_image"  # Replace with the actual IP address or hostname of your Raspberry Pi


@main.route('/send_image', methods=['GET'])
def send_image():
    # Open the image in binary mode
    if not os.path.exists(image_path):
        return jsonify({'error': 'Image file not found'}), 400

    with open(image_path, 'rb') as img_file:
        # Send the image as a POST request to the Raspberry Pi API
        files = {'file': img_file}
        response = requests.post(raspberry_pi_url, files=files)

    # If the response is successful, return the prediction from Raspberry Pi
    if response.status_code == 200:
        result = response.json()
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Failed to send or receive image', 'details': response.text}), 500

@main.route('/receive_image', methods=['POST'])
def receive_image():
    file = request.files['image']
    return "Image received!", 200

