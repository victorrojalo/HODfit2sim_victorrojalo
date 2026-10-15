#include <QCoreApplication>
#include <QDomDocument>
#include <QDebug>

int main(int argc, char *argv[]) {
    QCoreApplication app(argc, argv);

    QDomDocument doc;
    doc.setContent("<root><child>text</child></root>");
    qDebug() << "[QtXml Test] Root node:" << doc.documentElement().tagName();

    return 0;
}
