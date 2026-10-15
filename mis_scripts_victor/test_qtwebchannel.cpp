#include <QtWebChannel/QtWebChannel>

int main() {
    QWebChannel channel;
    return (channel.propertyUpdateInterval() != 0)? 0: 1;
}
