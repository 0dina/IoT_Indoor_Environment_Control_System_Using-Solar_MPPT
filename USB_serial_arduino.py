#include "DHT.h" // DHT 라이브러리 호출
DHT dht(10, DHT22); // DHT 설정(10, DHT22)
#include <LiquidCrystal.h>
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);
#define no_dust 0.60 // 최초 전원 인가 후 깨끗한 환경에서의 전압값

int dustout = A4; // 센서의 5번핀 먼지를 측정 아두이노 A4번에 연결
int v_led = A5; // 센서의 3번핀을 아두이노 A5번에 연결 (적외선 LED 제어)
int s_ledr = 13; // 공기 상태 나쁨 RED
int s_ledg = 12; // 공기 상태 보통 Green
int s_ledb = 11; // 공기 상태 좋음 Blue
float vo_value = 0; // 센서로 읽은 값 변수 선언
float sensor_voltage = 0; // 센서로 읽은 값을 전압으로 측정한 값
float dust_density = 0; // 실제 미세먼지 밀도

void setup() {
  Serial.begin(9600); // USB 시리얼 통신 시작
  dht.begin();
  pinMode(v_led, OUTPUT); // 적외선 LED 출력으로 설정
  pinMode(s_ledr, OUTPUT); // LED Red 출력 설정
  pinMode(s_ledg, OUTPUT); // LED Green 출력 설정
  pinMode(s_ledb, OUTPUT); // LED Blue 출력 설정
  lcd.begin(16, 2);
  lcd.setCursor(0, 0);
  lcd.clear();
  digitalWrite(v_led, LOW); // 적외선 LED ON
  digitalWrite(s_ledr, LOW);
  digitalWrite(s_ledb, LOW);
  digitalWrite(s_ledg, LOW);
}

void loop() {
  // 적외선 LED로 샘플링
  digitalWrite(v_led, LOW);
  delayMicroseconds(280);
  vo_value = analogRead(dustout);
  delayMicroseconds(40);
  digitalWrite(v_led, HIGH);
  delayMicroseconds(9680);

  // 전압 및 미세먼지 농도 계산
  sensor_voltage = get_voltage(vo_value);
  dust_density = get_dust_density(sensor_voltage);
  int dust_density1 = dust_density;

  // LCD에 미세먼지 값 출력
  lcd.clear();
  lcd.setCursor(0, 1);
  lcd.print("Dust:");
  lcd.setCursor(5, 1);
  lcd.print(dust_density1);
  lcd.setCursor(8, 1);
  lcd.print("[ug/m^3]");

  // 공기 상태에 따른 LED 제어
  if (dust_density <= 50) { // 50이하면 파란불
    digitalWrite(s_ledr, LOW);
    digitalWrite(s_ledb, HIGH);
    digitalWrite(s_ledg, LOW);
  } else if (dust_density <= 100) { // 100이하면 초록불
    digitalWrite(s_ledr, LOW);
    digitalWrite(s_ledb, LOW);
    digitalWrite(s_ledg, HIGH);
  } else { // 그 이상 빨간불
    digitalWrite(s_ledr, HIGH);
    digitalWrite(s_ledb, LOW);
    digitalWrite(s_ledg, LOW);
  }

  // USB 시리얼 포트로 미세먼지 값 전송
  Serial.print("Dust:");
  Serial.print(dust_density1);
  Serial.println("[ug/m^3]");

  delay(2000); // 2초 간격
}

float get_voltage(float value) {
  return value * 5.0 / 1024; // 아날로그 값을 전압 값으로 변환
}

float get_dust_density(float voltage) {
  return (voltage - no_dust) / 0.005; // 데이터 시트 기준 공식
}
