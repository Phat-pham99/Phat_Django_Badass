FROM 20.19-alpine
WORKDIR .

COPY . ./
COPY package.json package-lock.json ./

RUN npm install

EXPOSE 3000
ENTRYPOINT ["npm", "start"]
# CMD ["npm", "start"]
CMD ["npm", "run", "dev"]
# CMD ["npm", "run", "build"]
# CMD ["npm", "run", "serve"]
# CMD ["npm", "run", "test"]