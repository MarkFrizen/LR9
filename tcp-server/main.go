package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net"
	"time"
)

// Lr9TcpServer представляет TCP-сервер для обработки JSON-сообщений
type Lr9TcpServer struct {
	host string
	port string
}

// Request представляет входящее сообщение от клиента
type Request struct {
	Message string `json:"message"`
}

// Response представляет ответ сервера клиенту
type Response struct {
	Message   string `json:"message"`
	Timestamp string `json:"timestamp"`
}

// NewLr9TcpServer создаёт новый экземпляр сервера
func NewLr9TcpServer(host, port string) *Lr9TcpServer {
	return &Lr9TcpServer{
		host: host,
		port: port,
	}
}

// handleConnection обрабатывает подключение клиента в отдельной горутине
func (s *Lr9TcpServer) handleConnection(conn net.Conn) {
	defer conn.Close()

	reader := bufio.NewReader(conn)

	for {
		// Чтение сообщения от клиента (до новой строки)
		data, err := reader.ReadBytes('\n')
		if err != nil {
			log.Printf("Ошибка чтения от клиента %s: %v", conn.RemoteAddr(), err)
			return
		}

		// Парсинг JSON
		var req Request
		if err := json.Unmarshal(data, &req); err != nil {
			log.Printf("Ошибка парсинга JSON от клиента %s: %v", conn.RemoteAddr(), err)
			continue
		}

		// Формирование ответа с текущим временем
		resp := Response{
			Message:   req.Message,
			Timestamp: time.Now().Format("2006-01-02 15:04:05"),
		}

		// Сериализация ответа в JSON
		respData, err := json.Marshal(resp)
		if err != nil {
			log.Printf("Ошибка сериализации ответа: %v", err)
			continue
		}

		// Отправка ответа клиенту
		_, err = conn.Write(append(respData, '\n'))
		if err != nil {
			log.Printf("Ошибка записи клиенту %s: %v", conn.RemoteAddr(), err)
			return
		}

		log.Printf("Обработано сообщение от %s: %s", conn.RemoteAddr(), req.Message)
	}
}

// Start запускает сервер и слушает подключения
func (s *Lr9TcpServer) Start() error {
	addr := fmt.Sprintf("%s:%s", s.host, s.port)
	listener, err := net.Listen("tcp", addr)
	if err != nil {
		return fmt.Errorf("ошибка запуска сервера на %s: %w", addr, err)
	}
	defer listener.Close()

	log.Printf("Lr9TcpServer запущен на %s", addr)

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("Ошибка принятия подключения: %v", err)
			continue
		}

		log.Printf("Новое подключение от %s", conn.RemoteAddr())

		// Запуск обработки подключения в отдельной горутине
		go s.handleConnection(conn)
	}
}

func main() {
	host := flag.String("host", "localhost", "Хост для прослушивания")
	port := flag.String("port", "8080", "Порт для прослушивания")
	flag.Parse()

	server := NewLr9TcpServer(*host, *port)

	if err := server.Start(); err != nil {
		log.Fatalf("Ошибка сервера: %v", err)
	}
}
