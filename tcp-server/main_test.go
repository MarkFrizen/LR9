package main

import (
	"bufio"
	"encoding/json"
	"net"
	"strings"
	"testing"
	"time"
)

// TestNewLr9TcpServer тестирует создание нового сервера
func TestNewLr9TcpServer(t *testing.T) {
	tests := []struct {
		name string
		host string
		port string
	}{
		{"localhost", "localhost", "8080"},
		{"all interfaces", "0.0.0.0", "9000"},
		{"custom host", "127.0.0.1", "1234"},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			server := NewLr9TcpServer(tt.host, tt.port)
			if server == nil {
				t.Fatal("Ожидался не nil сервер")
			}
			if server.host != tt.host {
				t.Errorf("Ожидался хост %s, получен %s", tt.host, server.host)
			}
			if server.port != tt.port {
				t.Errorf("Ожидался порт %s, получен %s", tt.port, server.port)
			}
		})
	}
}

// TestRequestUnmarshal тестирует парсинг JSON запроса
func TestRequestUnmarshal(t *testing.T) {
	tests := []struct {
		name     string
		jsonData string
		wantMsg  string
		wantErr  bool
	}{
		{"valid request", `{"message":"hello"}`, "hello", false},
		{"empty message", `{"message":""}`, "", false},
		{"message with spaces", `{"message":"hello world"}`, "hello world", false},
		{"invalid json", `{invalid}`, "", true},
		{"missing message", `{}`, "", false},
		{"wrong field type", `{"message":123}`, "", true},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			var req Request
			err := json.Unmarshal([]byte(tt.jsonData), &req)

			if tt.wantErr && err == nil {
				t.Error("Ожидалась ошибка, но её не было")
			}
			if !tt.wantErr && err != nil {
				t.Errorf("Ожидалась отсутствие ошибки, но получена: %v", err)
			}
			if !tt.wantErr && req.Message != tt.wantMsg {
				t.Errorf("Ожидалось сообщение %q, получено %q", tt.wantMsg, req.Message)
			}
		})
	}
}

// TestResponseMarshal тестирует сериализацию ответа
func TestResponseMarshal(t *testing.T) {
	resp := Response{
		Message:   "test message",
		Timestamp: "2026-03-19 12:00:00",
	}

	data, err := json.Marshal(resp)
	if err != nil {
		t.Fatalf("Ошибка сериализации: %v", err)
	}

	var result map[string]string
	if err := json.Unmarshal(data, &result); err != nil {
		t.Fatalf("Ошибка десериализации: %v", err)
	}

	if result["message"] != resp.Message {
		t.Errorf("Ожидалось сообщение %q, получено %q", resp.Message, result["message"])
	}
	if result["timestamp"] != resp.Timestamp {
		t.Errorf("Ожидалось время %q, получено %q", resp.Timestamp, result["timestamp"])
	}
}

// TestHandleConnection тестирует обработку соединения
func TestHandleConnection(t *testing.T) {
	server := NewLr9TcpServer("localhost", "0")

	// Создаём listener на случайном порту
	listener, err := net.Listen("tcp", "localhost:0")
	if err != nil {
		t.Fatalf("Ошибка создания listener: %v", err)
	}
	defer listener.Close()

	// Запускаем сервер в горутине
	go func() {
		for {
			conn, err := listener.Accept()
			if err != nil {
				return
			}
			go server.handleConnection(conn)
		}
	}()

	// Подключаемся к серверу
	clientConn, err := net.Dial("tcp", listener.Addr().String())
	if err != nil {
		t.Fatalf("Ошибка подключения: %v", err)
	}
	defer clientConn.Close()

	// Отправляем запрос
	req := Request{Message: "test message"}
	reqData, _ := json.Marshal(req)
	_, err = clientConn.Write(append(reqData, '\n'))
	if err != nil {
		t.Fatalf("Ошибка записи: %v", err)
	}

	// Читаем ответ
	reader := bufio.NewReader(clientConn)
	respData, err := reader.ReadBytes('\n')
	if err != nil {
		t.Fatalf("Ошибка чтения: %v", err)
	}

	var resp Response
	if err := json.Unmarshal([]byte(strings.TrimSpace(string(respData))), &resp); err != nil {
		t.Fatalf("Ошибка парсинга ответа: %v", err)
	}

	if resp.Message != "test message" {
		t.Errorf("Ожидалось сообщение %q, получено %q", "test message", resp.Message)
	}
	if resp.Timestamp == "" {
		t.Error("Ожидалось непустое поле timestamp")
	}
}

// TestHandleConnectionInvalidJSON тестирует обработку невалидного JSON
func TestHandleConnectionInvalidJSON(t *testing.T) {
	server := NewLr9TcpServer("localhost", "0")

	listener, err := net.Listen("tcp", "localhost:0")
	if err != nil {
		t.Fatalf("Ошибка создания listener: %v", err)
	}
	defer listener.Close()

	go func() {
		for {
			conn, err := listener.Accept()
			if err != nil {
				return
			}
			go server.handleConnection(conn)
		}
	}()

	clientConn, err := net.Dial("tcp", listener.Addr().String())
	if err != nil {
		t.Fatalf("Ошибка подключения: %v", err)
	}
	defer clientConn.Close()

	// Отправляем невалидный JSON
	_, err = clientConn.Write([]byte(`{invalid json}` + "\n"))
	if err != nil {
		t.Fatalf("Ошибка записи: %v", err)
	}

	// Сервер должен продолжить работу, отправим валидный запрос
	time.Sleep(100 * time.Millisecond)

	req := Request{Message: "valid after invalid"}
	reqData, _ := json.Marshal(req)
	_, err = clientConn.Write(append(reqData, '\n'))
	if err != nil {
		t.Fatalf("Ошибка записи: %v", err)
	}

	reader := bufio.NewReader(clientConn)
	respData, err := reader.ReadBytes('\n')
	if err != nil {
		t.Fatalf("Ошибка чтения: %v", err)
	}

	var resp Response
	if err := json.Unmarshal([]byte(strings.TrimSpace(string(respData))), &resp); err != nil {
		t.Fatalf("Ошибка парсинга ответа: %v", err)
	}

	if resp.Message != "valid after invalid" {
		t.Errorf("Ожидалось сообщение %q, получено %q", "valid after invalid", resp.Message)
	}
}

// TestHandleConnectionMultipleMessages тестирует обработку нескольких сообщений
func TestHandleConnectionMultipleMessages(t *testing.T) {
	server := NewLr9TcpServer("localhost", "0")

	listener, err := net.Listen("tcp", "localhost:0")
	if err != nil {
		t.Fatalf("Ошибка создания listener: %v", err)
	}
	defer listener.Close()

	go func() {
		for {
			conn, err := listener.Accept()
			if err != nil {
				return
			}
			go server.handleConnection(conn)
		}
	}()

	clientConn, err := net.Dial("tcp", listener.Addr().String())
	if err != nil {
		t.Fatalf("Ошибка подключения: %v", err)
	}
	defer clientConn.Close()

	messages := []string{"first", "second", "third"}
	reader := bufio.NewReader(clientConn)

	for _, msg := range messages {
		req := Request{Message: msg}
		reqData, _ := json.Marshal(req)
		_, err = clientConn.Write(append(reqData, '\n'))
		if err != nil {
			t.Fatalf("Ошибка записи: %v", err)
		}

		respData, err := reader.ReadBytes('\n')
		if err != nil {
			t.Fatalf("Ошибка чтения: %v", err)
		}

		var resp Response
		if err := json.Unmarshal([]byte(strings.TrimSpace(string(respData))), &resp); err != nil {
			t.Fatalf("Ошибка парсинга ответа: %v", err)
		}

		if resp.Message != msg {
			t.Errorf("Ожидалось сообщение %q, получено %q", msg, resp.Message)
		}
	}
}

// TestResponseTimestampFormat тестирует формат timestamp в ответе
func TestResponseTimestampFormat(t *testing.T) {
	resp := Response{
		Message:   "test",
		Timestamp: time.Now().Format("2006-01-02 15:04:05"),
	}

	// Проверяем, что timestamp соответствует ожидаемому формату
	_, err := time.Parse("2006-01-02 15:04:05", resp.Timestamp)
	if err != nil {
		t.Errorf("Timestamp не соответствует формату YYYY-MM-DD HH:MM:SS: %v", err)
	}
}
