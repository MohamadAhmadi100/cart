<div id="top"></div>
<!--
*** Authord by ErfanR.
--> 
   
<!-- Website LOGO -->
<br />
<div align="center">
  <a href="https://aasood.com">
    <img src="https://aasood.com/media/logo/stores/1/file.png" alt="Logo" width="107" height="47">
  </a>

<h3 align="center">Cart Microservice</h3>

  <p align="center">
    A microservice to manage user cart!
    <br />
    <a href="#"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://devcart.aasood.com/api/v1/docs">View Demo</a>
    ·
    <a href="https://gitlab.aasood.com/ecommerce/backend/cart/-/issues">Report Bug</a>
    ·
    <a href="https://gitlab.aasood.com/ecommerce/backend/cart/-/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Road map</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->

## About The Project

As a microservice based project, according to the contractor desire, we needed a service for managing user cart. So we
created a microservice for this purpose!

This microservice will do:

* add or edit an item in user's cart
* remove an item from user's cart
* And at last get the cart of a user :smile:

We have specified a schema for adding item to cart; Here is an example:

```json
{
  "parent_system_code": "10010100201",
  "system_code": "100101002001",
  "storage_id": "1",
  "count": 1
}
```

Let me explain each one individually:

* `parent_system_code`: This is the parent system code of the item.
* `system_code` is a required key of **product** that is unique.
* `count` is the number you want your given product in the cart.
* `storage_id` is the id of a storage that user want to buy the product from

And another schema for cart in the database; Here is an example:

```json
{
  "user_info": {
    "user_id": 84
  },
  "products": [
    {
      "status": "in_cart",
      "count": 2,
      "storage_id": "3",
      "price": 50000000,
      "system_code": "100104001018",
      "visible_in_site": true,
      "config": {
        "storage": {
          "value": "64 GB",
          "attribute_label": "حافظه داخلی",
          "label": "۶۴ گیگابایت"
        },
        "color": {
          "value": "blue",
          "attribute_label": "رنگ",
          "label": "آبی"
        },
        "guarantee": {
          "value": "awat",
          "attribute_label": "گارانتی",
          "label": "آوات"
        },
        "ram": {
          "value": "4 GB",
          "attribute_label": "رم",
          "label": "۴ گیگابایت"
        },
        "seller": {
          "value": "Awat",
          "attribute_label": "فروشنده",
          "label": "آوات"
        }
      }
    }
  ]
}
```

Let me explain each one individually:

* `user_info` is a dictionary of a user informations.
    * `user_id` is a required key of **user_info** that is unique.
* `product` is a dictionary of a product informations.
    * `system_code` is a required key of **product** that is unique.
    * `count` is the number of the product in the cart.
    * `storage_id` is the id of a storage that the product is from
    * `price` is the current price of the the product.
    * `status` is the status of the product

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

This section should list any major frameworks/libraries used to bootstrap your project. Leave any add-ons/plugins for
the acknowledgements section. Here are a few examples.

* [Python](https://www.python.org)
* [Mongo DB](https://www.mongodb.com)
* [RabbitMQ](https://www.rabbitmq.com)
* Later, [Vue.js](https://vuejs.org) may included.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->

## Getting Started

In this part, there is an instructions on setting up the project locally. To get a local copy up and running follow
these simple steps.

### Prerequisites

For this project, you need python v3.9 and mongodb
v5[Install MongoDB Community Edition](https://docs.mongodb.com/manual/administration/install-community/)

### Installation

After installing prerequisites, now you can install dependencies of this project:

1. Clone the repo
   ```sh
   git clone http://200.100.100.162/ecommerce/backend/cart.git
   ```
2. Setup an environment
    ```sh
    sudo apt install python3-virtualenv
    virtualenv venv
    source venv/bin/activate
    ```
3. Install pip packages
   ```sh
   pip install -r requirements.txt
   ```
4. In main directory(where `setup.py` file is) use this command to install the project
   ```sh
   pip install -e .
   ```
5. Create .env file in main directory
    ```buildoutcfg
   
    APP_NAME='cart'
   
    MONGO_USER=''
    MONGO_PASS=''
    MONGO_HOST='localhost'
    MONGO_DB='db_cart'
   
    RABBIT_HOST='localhost'
    ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->

## Usage

To run the project, make sure that the mongodb service is up locally and run this in the app directory

```sh
python main.py
```

- You can visit [localhost:8000](http://localhost:8000) for root directory.

<p align="right">(<a href="#top">back to top</a>)</p>

## Database Visualization

Download mongodb compass:
[MongoDB Compass](https://www.mongodb.com/try/download/compass)

## Testing

For testing the project, run this command in main directory

```sh
pytest
```

#### Coverage

Testing coverage can also be achieved by:

```shell
pytest --cov
```

<!-- ROADMAP -->

## Roadmap

- [x] CRUD
- [ ] Refactor according to needs

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any
contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also
simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->

## License

All rights reserved

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->

## Contact

* Meisam Taghizadeh - [@meisam2236](https://t.me/meisam2236) - meisam2236@gmail.com
* Erfan Rezaee - rezaee.e2002@gmail.com

Project Link: [https://gitlab.aasood.com/ecommerce/backend/cart](https://gitlab.aasood.com/ecommerce/backend/cart)

<p align="right">(<a href="#top">back to top</a>)</p>

