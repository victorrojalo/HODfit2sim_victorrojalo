#include <QWebSocket>
#include <QString>

int main() {
    QWebSocket ws;
    QString s("");
    return (ws.errorString() == "")? 0: 1;
}
