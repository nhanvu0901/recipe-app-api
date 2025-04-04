import numpy as np
class testIlterator:
    def __init__(self, max_data):
        self.max_data = max_data
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.max_data:
            value = self.current
            self.current += 1
            return value
        raise StopIteration

iterator = testIlterator(5)

# np_array = np.array([1, 2, 3, 4, 5])
#
# # NumPy arrays cũng là iterable
# np_iter = iter(np_array)
# print(next(np_iter))  # 1

squares_list = [x*x for x in range(1000)]  # Chiếm nhiều bộ nhớ

# Generator expression (tạo các giá trị theo yêu cầu)
squares_gen = (x*x for x in range(1000))   # Tiết kiệm bộ nhớ

def echo_generator():
    value = yield 'Hãy nhập giá trị'
    while True:
        yield f'Bạn đã gửi {value}'

# gen = echo_generator()
# print(next(gen))  # Khởi động generator: 'Sẵn sàng nhận giá trị'
# print(gen.send('Hello'))  # Gửi 'Hello' và nhận phản hồi: 'Bạn đã gửi: Hello'
# print(gen.send(42))  # Gửi 42 và nhận phản hồi: 'Bạn đã gửi: 42'

# my_list = [1, 2, 3, 4, 5, 6]
# iterator = iter(my_list)
# print(next(iterator))
# print(next(iterator))

#Context manager
class MyContextManager:
    def __init__(self):
        print("Start resources")
    def __enter__(self):
        print("Vào khối with - thiet lập tài nguyên")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Thoát khỏi khối with - Dọn dẹp tài nguyên")
        if exc_tb is not None:
            print(f"Có lỗi xảy ra: {exc_val}")
        return True

# with MyContextManager() as cm:
# #     print("Đang làm việc trong khối with")
# #     # Giả lập một lỗi
# #     raise Exception("Oops, có lỗi!")


#tuple is an immutable data type
genres_tuple = ("Pop", "Rock", "Hip Hop", "Jazz", "Classical", "Electronic", "Country", "R&B","disco")
print(len(genres_tuple))

print(genres_tuple[3:6])
first_two = genres_tuple[:2]
print(first_two)
disco_index = genres_tuple.index("disco")
print(disco_index)
C_tuple = (-5, 1, -3)
sorted = sorted(C_tuple)
print(sorted)