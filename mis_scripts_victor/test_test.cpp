#include <QtTest>

class DummyTest : public QObject {
    Q_OBJECT
private slots:
    void passTest() {
        QVERIFY(true);
    }
};

QTEST_MAIN(DummyTest)
#include "test_test.moc"
