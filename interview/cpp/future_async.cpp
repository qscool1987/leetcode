#include <future>
#include <iostream>
#include <thread>


long long add(long long n) {
    long long sum = 0;
    for(long long  i = 0; i <= n; ++i) {
        sum += i;
    }
    return sum;
}

long long add2(long long n) {
    long long sum = 0;
    for(long long  i = 100; i <= n; ++i) {
        sum += i;
    }
    return sum;
}

int sub(int a, int b) {
    return a - b;
}

int main() {
    std::future<long long> future1 = std::async(add, 1000000000); //异步执行add，不阻塞当前线程
    std::packaged_task<long long(long long)> task(add2); //对函数进行包装
    std::future<long long> future2 = task.get_future();
    task(100000);
    std::cout << sub(10,5) << std::endl;
    std::cout << "wait..." << std::endl;
    std::cout << future1.get() << std::endl; // 阻塞当前线程
    std::cout << "add finished" << std::endl;
    std::cout << future2.get() << std::endl;
    return 0;
}