#include<iostream>
#include <thread>
#include <mutex>
using namespace std;

/*
    单例模式 只要考查设计模式，该知识点必考
    1.懒汉，饿汉模式区别
    2.线程安全性如何保证
    3.效率如何保证
*/

// 懒汉模式
class Singleton {
public:
    static Singleton* getInstance() {
        if (_p == nullptr) { // double check保证效率
            std::lock_guard<mutex> gard(_lock); // 锁保证线程安全
            if (_p == nullptr) {
                _p = new Singleton();
            }
        }
        return _p;
    }

private:
    Singleton() {cout << "Singleton1" << endl;}
    Singleton(const Singleton&) {}
    Singleton& operator = (const Singleton&) {}
    static Singleton* _p;
    static mutex _lock;
};

Singleton* Singleton::_p = nullptr;
mutex Singleton::_lock;

// 饿汉模式
class Singleton2 {
public:
    static Singleton2* getInstance() {
        
        return &obj;
    }

private:
    Singleton2() {cout << "Singleton2" << endl;}
    Singleton2(const Singleton2&) {}
    Singleton2& operator = (const Singleton2&) {}
    static Singleton2 obj;
};

Singleton2 Singleton2::obj;

int main() {
    
    cout << "fuck" << endl;
    auto o1 = Singleton::getInstance();
    auto o2 = Singleton2::getInstance();
    cout << "hellox" << endl;
    return 0;
}