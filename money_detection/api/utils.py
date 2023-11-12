def get_bounding_boxes_yolov8(img_path, model):
    detections = model(img_path)
    confs = detections[0].boxes.conf
    classes = detections[0].boxes.cls
    boxes = detections[0].boxes.xyxy
    conf_thr = 0.0
    bounding_boxes = []
    for elem in zip(boxes, classes, confs):
        top_left = (int(elem[0][0]), int(elem[0][1]))
        bottom_right = (int(elem[0][2]), int(elem[0][3]))
        label = str(int(elem[1]))
        conf = float(elem[2])
        # Convert int value labels to their corresponding classes:
        if label == "0":
            label = "real"
        elif label == "1":
            label = "dolar"
        elif label == "2":
            label = "euro"
        # Filter low-confidence detections:
        if conf > conf_thr:
            bounding_boxes.append(([top_left, bottom_right], label, conf))
        print("BBS:")
        print(bounding_boxes)
    return bounding_boxes


def crop_image_by_bounding_boxes(img, bounding_boxes):
    cropped_images = []
    for bounding_box in bounding_boxes:
        if len(bounding_box) != 0:
            cropped_image = img[bounding_box[0][0][1]:bounding_box[0][1][1], bounding_box[0][0][0]:bounding_box[0][1][0]]
            cropped_images.append(cropped_image)
    return cropped_images