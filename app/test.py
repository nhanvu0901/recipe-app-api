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

gen = echo_generator()
print(next(gen))  # Khởi động generator: 'Sẵn sàng nhận giá trị'
print(gen.send('Hello'))  # Gửi 'Hello' và nhận phản hồi: 'Bạn đã gửi: Hello'
print(gen.send(42))  # Gửi 42 và nhận phản hồi: 'Bạn đã gửi: 42'