class SalesRecord:

    def __init__(self, invoice_no, stock_code, description, quantity, invoice_date, unit_price, customer_id, country):
        """Class that identifies a Sales record from the Online_retail_II dataset"""
                
        self.invoice_no = invoice_no
        self.stock_code = stock_code
        self.description = description
        self.quantity = quantity
        self.invoice_date = invoice_date
        self.unit_price = unit_price
        self.customer_id = customer_id
        self.country = country

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}(inv_no={self.invoice_no}, inv_date={self.invoice_date}, cust_id={self.customer_id}, cntry={self.country}, stock_cd={self.stock_code}, price={self.unit_price}, qty={self.quantity})"
    
    def __str__(self):
        return f"Invoice {self.invoice_no}: {self.quantity}x {self.description} @ ${self.unit_price}=${self.revenue} ({self.country})"
    

    @property
    def unit_price(self):
        return self._unit_price
    
    @unit_price.setter
    def unit_price(self, value):
        if value<0:
            raise ValueError('unit_price must be a non-negative number.')
        self._unit_price = value

    @property
    def revenue(self):
        return self.unit_price*self.quantity
    
    @property
    def is_return(self):
        return self.quantity<0
    
    @classmethod
    def from_dict(cls, d):
        return cls(**d)
    
    @staticmethod
    def is_valid_invoice_no(invoice_no):
        return len(invoice_no)>0 and str.isalnum(invoice_no)
    
    def to_dict(self):
        d = self.__dict__.copy()
        d['unit_price'] = d.pop('_unit_price')  #fix the name because now it s saved with the underscore
        return d
    
    def apply_discount(self,pct):
        self.unit_price = self.unit_price-(self.unit_price*pct/100)




class ReturnRecord(SalesRecord):
    """Class that identifies entries correspomdimg to returns."""

    def __init__(self, invoice_no, stock_code, description, quantity, invoice_date, unit_price, customer_id, country, reason):
        super().__init__(invoice_no, stock_code, description, quantity, invoice_date, unit_price, customer_id, country)
        self.reason = reason

    def __str__(self):
        return f"Return {self.invoice_no}:{self.quantity}x {self.description} @ ${self.unit_price} | Reason: {self.reason} ({self.country})"

    def __repr__(self):
        parent_repr = super().__repr__().rstrip(')')    # remove closing parenthesis
        return f"{parent_repr}, reason='{self.reason}')"
        # could have also been done by rewriting all


    def to_dict(self):  # override to include reason
        d = super().to_dict()
        d['reason'] = self.reason
        return d

    def apply_discount(self, pct):
        raise TypeError("No discount can be applied on returns.")
    


class Invoice:
    def __init__(self, invoice_no, customer_id):
        self.invoice_no = invoice_no
        self.customer_id = customer_id
        self.records = []          # empty list, will contain SalesRecord objects


    def __len__(self):
        return len(self.records)

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}(number={self.invoice_no},cust_id={self.customer_id})"

    def __str__(self):
        return f"Invoice no. {self.invoice_no}: {self.item_count()} records, total revenue={self.total_revenue()}"

    def __iter__(self):
        return iter(self.records)  # allows to use for record in invoice etc
    
    def add_record(self, record):
        if not isinstance(record, SalesRecord):
            raise TypeError("record must be a SalesRecord instance.")
        self.records.append(record)   # same as my_list.append(r1)
    
    def total_revenue(self):
        return sum(record.revenue for record in self.records)  # loop over the objects

    def item_count(self):
        return sum(record.quantity for record in self.records)

    def summary(self):
        ret = 0
        for record in self:
            if record.is_return:
                ret+=1

        d = {"total_revenue":self.total_revenue(), "item_count":self.item_count(), "n_records":len(self), "n_returns":ret}
        return d