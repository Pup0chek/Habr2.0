# frontend/Dockerfile

FROM node:14

WORKDIR /app

# Копируем package.json и устанавливаем зависимости
COPY package.json . 
RUN npm install

# Копируем оставшийся исходный код
COPY . .

# Запускаем приложение
CMD ["npm", "start"]
