import tkinter
from PIL import Image, ImageTk

class TransparentWindow():
    """透過画面"""

    FRAME_OFFSET = -2
    BG_COLOR = "magenta"

    def __init__(self, main, images, position=(0, 0)):
        """コンストラクタ"""
        self.main = main
        main.config(bg=self.BG_COLOR)
        
        # 複数の画像をリストとして受け取る
        self.images = images
        self.current_index = 0
        self.image = self.images[self.current_index]
        
        self.window_position = position
        self.window_size = (self.image.width, self.image.height)

        self.main.geometry(str(self.window_size[0]) + "x" +
                           str(self.window_size[1]) + "+" +
                           str(self.window_position[0]) + "+" +
                           str(self.window_position[1]))

        self.main.wm_overrideredirect(True)
        # 透過表示(くり抜き)色を指定
        self.main.wm_attributes("-transparentcolor", self.BG_COLOR)

        self.init_canvas(self.main, self.image)

        # 画像切り替えのインターバル（ミリ秒）を設定し、ループ開始
        self.change_interval = 100
        self.update_image()

    def init_canvas(self, frame, image):
        """canvas初期化"""
        # canvas作成
        self.canvas = tkinter.Canvas(
            frame,
            width=image.width,
            height=image.height,
            bg=self.BG_COLOR,
            highlightthickness=0 # 枠線を完全に消す推奨設定
        )

        # 枠を消すためにマイナス値を指定
        self.canvas.place(x=self.FRAME_OFFSET, y=self.FRAME_OFFSET)

        # PIL.Image から PhotoImage 生成
        self.photo_image = ImageTk.PhotoImage(image=image)

        # canvasに画像を表示し、IDを保持（後で書き換えるため）
        self.image_id = self.canvas.create_image(
            self.photo_image.width() / 2,
            self.photo_image.height() / 2,
            image=self.photo_image
        )

    # 画像を切り替える処理
    def update_image(self):
        """画像を次のものに更新する"""
        # 次の画像のインデックスを計算（最後まで行ったら0に戻る）
        self.current_index = (self.current_index + 1) % len(self.images)
        next_image = self.images[self.current_index]

        # 新しい画像を PhotoImage に変換
        self.photo_image = ImageTk.PhotoImage(image=next_image)

        # Canvas上の画像を新しいものに書き換え
        self.canvas.itemconfig(self.image_id, image=self.photo_image)

        # 指定時間後（change_interval）に、再度この関数を呼び出す
        self.main.after(self.change_interval, self.update_image)


if __name__ == '__main__':
    # 切り替えたい画像のファイル名をリストで指定
    image_files = ["./risa1.png", "./risa2.png", "./risa3.png"] 
    
    pil_images = []
    
    for file in image_files:
        try:
            # 画像ファイルを開く
            img = Image.open(file)
            # サイズ調整 1/6
            img = img.resize(
                (int(img.width / 6), int(img.height / 6)),
                Image.NEAREST
            )
            pil_images.append(img)
        except Exception as e:
            print(f"画像 {file} の読み込みに失敗しました: {e}")

    # 画像が1枚も読み込めなかった場合は終了
    if not pil_images:
        print("表示する画像がありません。")
        exit()

    # 透過画面表示
    root = tkinter.Tk()
    # 最前面固定
    root.attributes("-topmost", True)

    # 基準となるサイズ（1枚目の画像）で位置を計算
    base_width = pil_images[0].width
    base_height = pil_images[0].height
    
    window_position = (root.winfo_screenwidth() - base_width - 25,
                       root.winfo_screenheight() - base_height - 50)

    # クラスの呼び出し（画像リストを渡すように変更）
    TransparentWindow(main=root,
                      images=pil_images,
                      position=window_position)
                      
    root.mainloop()