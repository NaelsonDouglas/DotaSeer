FROM bayesimpact/react-base
COPY . /app
WORKDIR /app
CMD ["npm", "start"]
RUN yarn install
ENTRYPOINT [ "yarn", "start" ]