# Copyright 2019 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, models
from odoo.tools.float_utils import float_round


class InvaderPayable(models.AbstractModel):

    _name = "invader.payable"
    _description = "Interface for payable objects (e.g. cart, ...)"

    def _invader_prepare_payment_transaction_data(self, acquirer_id):
        """
        Prepare a dictionary to create a ``payment.transaction`` for the
        correct amount and linked to the payable object.

        :param acquirer_id: ``payment.acquirer`` record
        :return: dictionary suitable for ``payment.transaction`` ``create()``
        """

    def _invader_get_transactions(self):
        """
        Return payment transaction recordset depending on the payable model
        """

    def _get_payable_lines(self):
        """
        Return payable lines
        """

    @api.model
    def _get_formatted_amount(self, transaction, amount):
        """
        The expected amount format by Adyen
        :param amount: float
        :return: int
        """
        dp_name = transaction.acquirer_id.provider or ""
        if dp_name:
            dp_name = dp_name.capitalize()
        digits = self.env["decimal.precision"].precision_get(dp_name)
        return float_round(amount, digits)
