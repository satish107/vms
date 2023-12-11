## VMS

Develop a Vendor Management System using Django and Django REST Framework. This system will handle vendor profiles, track purchase orders, and calculate vendor performance metrics.


# Tech/framework used
- [Python](https://www.python.org/)
- [Django Rest Framework](https://www.django-rest-framework.org/)

# Installation
- Clone the code
- git clone git@github.com:satishkmr632/vms.git
- Create a virtual environment and install the requirements.
- python3 -m venv env && source env/bin/activate
- pip install -r requirements.txt
- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser
- python manage.py runserver


# Test Case:
- All the apis of VMS are secured with token(JWT).
- 1.Create an user who will have access to all apis of VMS.
	- Api: "api/1/register"
	- Type: "POST"
	- Payload:
		{
			"username": "satish",
			"password": "test@123"
		}
	- Response:
		{
		    "username": "satish"
		}
- 2.Login with the credetials
	- Api: "api/1/login"
	- Type: "POST"
	- Payload:
		{
			"username": "satish",
			"password": "test@123"
		}
	- Response:
		{
		    "username": "satish",
		    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAyMjQ3MTQ1LCJpYXQiOjE3MDIyNDY1NDUsImp0aSI6ImEzZWVlZjFlOTcyOTQyMjZhOWI2YWI1NjQyY2M4NzFlIiwidXNlcl9pZCI6MX0.aI6s-zSK-YwAvzFOUSR7FIhq-vLc9LRKyJPVT0DnuGE",
		    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMjMzMjk0NSwiaWF0IjoxNzAyMjQ2NTQ1LCJqdGkiOiI4MmJhY2RhM2VhMmU0OWYxOTljMzMzYjYyNzNmNGNhNSIsInVzZXJfaWQiOjF9.WM2UcStZDG5MpUHiuBgPRxy5Qjg8IuzvSxAu126lT9w"
		}

- 3. Pass the access_token in headers of every request as Authorization Key.
	Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAyMjQ3MTQ1LCJpYXQiOjE3MDIyNDY1NDUsImp0aSI6ImEzZWVlZjFlOTcyOTQyMjZhOWI2YWI1NjQyY2M4NzFlIiwidXNlcl9pZCI6MX0.aI6s-zSK-YwAvzFOUSR7FIhq-vLc9LRKyJPVT0DnuGE

	if token expires create another one by login again, as access_token life is 30 Mins.

- 4. Create Vendor

	- Api: "api/1/vendors" (Create vendor)
	- Type: "POST"
	- Payload:
		{
		    "name": "vendor 1",
		    "contact_details": "contact_details 1",
		    "address": "address 1"
		}

	- Api: "api/1/vendors" (List all vendors)
	- Type: "GET"

	- Api: "api/1/vendors/1" (specific vendor)
	- Type: "GET"

	- Api: "api/1/vendors/1" (Update Vender)
	- Type: "PUT"
	- Payload:
	{
	    "name": "vendor 1",
	    "contact_details": "changed contact_details 1",
	    "address": "address 1"
	}

	Api: "api/1/vendors/1"
	Type: "DELETE"

- 5. Create Purchase Order or assign an order to vendor.
	
	- Api: "api/1/purchase_orders" (Create purchase order)
	Type: "POST"
	Payload:
		{
			"vendor": 1,
			"expected_delivery_date": "2023-12-7T19:54:37.710051Z",
			"actual_delivery_date": "2023-12-9T19:54:37.710051Z",
			"items": {"products": "Mobile"},
			"quantity": 1
		}

	- Api: "api/1/purchase_orders" (List all purchase orders)
	Type: "GET"

	- Api: "api/1/purchase_orders/1" (specific purchase order)
	Type: "GET"

	- Api: "api/1/purchase_orders/1" (Update purchase order)
	- Type: "PUT"
	- Payload:
	{
		"vendor": 1,
		"expected_delivery_date": "2023-12-7T19:54:37.710051Z",
		"actual_delivery_date": "2023-12-9T19:54:37.710051Z",
		"items": {"products": "Mobile"},
		"quantity": 1
	}

	- Api: "api/1/purchase_orders/1"
	- Type: "DELETE"


- 6. Add Required field to update. purchase order update api.
	- a) vendors On-Time Delivery Rate updated on every time status is marked as completed. For This
		add expected_delivery_date, actual_delivery_date in purchase_order or status=3 in purchase order update api.
		{
			"vendor": 1,
			"expected_delivery_date": "2023-12-7T19:54:37.710051Z",
			"actual_delivery_date": "2023-12-9T19:54:37.710051Z",
			"items": {"products": "Mobile"},
			"quantity": 1,
			"status": 3
		}
	- b) Quality Rating Average:
		if Quality Rating and order status is completed then calculate Average value of Quality Rating of the vendor.
		{
			"vendor": 1,
			"quality_rating": 5.0,
			"status": 3
		}

	- c) Average Response Time:
		First update po with issue date
		{
			"vendor": 1,
			"issue_date": "2023-12-9T19:54:37.710051Z"
		}
		Then acknowledge this po by calling "api/1/purchase_orders/1/acknowledge" (POST)
		No data required.

		find difference between acknowledge_date and issue date to caclculate avg_response_time
	
	- d) Fulfilment Rate:
		Any Change in PO status, Fulfilment Rate is updates
		we can use the po's update api
