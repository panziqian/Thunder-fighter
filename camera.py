import cv2
import numpy as np

def face_detection():
    # 加载人脸检测器
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')
    # 打开摄像头
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("unable to capture frame")
            break
        # 转为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 检测人脸
        faces = face_cascade.detectMultiScale(
            gray,  #待识别的灰度图像
            scaleFactor=1.1, #缩放比例
            minNeighbors= 3, #检测框的最小邻居数（越高，误检越少，但可能漏检）
            minSize = (50,50) #最小的人脸
        )
        # 绘制人脸框
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 0)
            print((x, y), (x + w, y + h))
        # 显示结果
        cv2.imshow('Face Detection', frame)
        # 按ESC键退出
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

def test_camera():
    max_tested=3
    available_camera=[]
    for i in range(max_tested):
        cap=cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"available camera {i} detected")
            width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            height=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            fps=cap.get(cv2.CAP_PROP_FPS)
            print(f"width:{width} height:{height} fps:{fps}")
            available_camera.append(cap)
            cap.release()
        else:
            print(f"camera {i} is not available")

def dnn():
    # 加载Caffe模型
    model_weights = "./models/res10_300x300_ssd_iter_140000.caffemodel"
    model_config = "./models/deploy.prototxt"
    net = cv2.dnn.readNetFromCaffe(model_config, model_weights)
    #启动gpu加速(目前不可用)
    #net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    #net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

    def detect_faces_dnn(image, min_confidence=0.5):
        """
        使用DNN检测人脸
        :param image: 输入图像（BGR格式）
        :param min_confidence: 置信度阈值
        :return: 带检测框的图像
        """
        (h, w) = image.shape[:2]
        # 预处理：缩放 + 均值减法 (104, 177, 123)
        blob = cv2.dnn.blobFromImage(
            cv2.resize(image, (300, 300)),
            scalefactor=1.0,
            size=(300, 300),
            mean=(104.0, 177.0, 123.0)
        )
        # 输入网络并获取检测结果
        net.setInput(blob)
        detections = net.forward()
        # 绘制检测框
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > min_confidence:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                print((startX, startY), (endX, endY))
                # 绘制矩形和置信度
                text = "{:.2f}%".format(confidence * 100)
                y = startY - 10 if startY - 10 > 10 else startY + 10
                cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
                cv2.putText(image, text, (startX, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        return image
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        output = detect_faces_dnn(frame)
        cv2.imshow("Real-Time DNN Face Detection", output)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    test_camera()
    #face_detection()
    #dnn()