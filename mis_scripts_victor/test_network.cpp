#include <QCoreApplication>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QNetworkRequest>

int main(int argc, char *argv[]) {
    QCoreApplication app(argc, argv);

    QNetworkAccessManager manager;
    manager.setTransferTimeout(30);

    QNetworkRequest req(QUrl("https://httpbin.org/get"));

    QNetworkReply *reply = manager.get(req);

    QObject::connect(reply, &QNetworkReply::finished, [&]() {
        qDebug() << "[QtNetwork Test] Network reply: " << reply->readAll();
        app.quit();
    });

    return app.exec();
}
