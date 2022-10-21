#include <iostream>
#include <list>
#include <unordered_map>
#include <atomic>

/*
    LRU是各大公司常考的面试题，此处提供一个模版类，并支持线程安全
    线程安全通过atomic原子操作来控制
*/

template<typename T>
struct Node {
    Node() {}
    Node(const T &t, int key): _t(t), _key(key) {}
    T _t;
    int _key;
};

template<typename T>
class LRU {
public:
    LRU() {}
    LRU(int cap): _cap(cap) {}
    void push(const T &t, int key) {
        // not in
        while (_lock.test_and_set()) {}
        if (table.count(key) > 0) {
            que.erase(table[key]);
        }
        que.push_front(Node<T>(t, key));
        table[key] = que.begin();
    
        //in
        if (que.size() > _cap) {
            auto _iter = --que.end();
            int key = _iter->_key;
            que.erase(_iter);
            table.erase(key);
        }
        _lock.clear();
    }
    bool get(int key, T &val) {
        if (table.count(key) == 0) {
            return false;
        }
        val = table[key]->_t;
        que.erase(table[key]);
        que.push_front(Node<T>(val, key));
        table[key] = que.begin();
        return true;
    }

    void show() {
        for(auto& m : que) {
            std::cout << m._key << "->" << m._t << ", ";
        }
        std::cout << std::endl;
    }
    
private:
    std::unordered_map<int, typename std::list<Node<T>>::iterator> table;
    std::list<Node<T>> que;
    int _cap = 5; // 缓存容量
    std::atomic_flag _lock = ATOMIC_FLAG_INIT; // 保证线程安全
};




int main() {
    LRU<int> lru;
    lru.push(1,2);
    lru.show();
    lru.push(2,4);
    lru.push(3,5);
    lru.push(2,4);
    lru.push(3,10);
    lru.push(7,7);
    lru.push(7,8);
    lru.show();
    int m;
    if (lru.get(3, m)) {
        std::cout << "key=3,val=" << m << std::endl;
    }
    if (lru.get(5, m)) {
        std::cout << "key=5,val=" << m << std::endl;
    }
    return 0;
}
