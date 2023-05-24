from odoo import api, fields, models
from datetime import datetime, timedelta


class ProductionReportXlsx(models.AbstractModel):
    _name = "report.solinda_mrp.report_service"
    _inherit = "report.report_xlsx.abstract"

    def generate_xlsx_report(self, workbook, data, objs):
        datas = data.get("form", {})
        mp_ids = (
            self.env["mrp.workorder"]
            .sudo()
            .search(
                [
                    ("po_date", ">=", datas.get("start_date")),
                    ("po_date", "<=", datas.get("end_date")),
                    ("state", "in", ["progress", "ready", "done"]),
                    ("supplier", "in", datas.get("supplier")),
                    ("workcenter_id", "=", datas.get("service")),
                ]
            )
        )

        title_workcenter = (
            self.env["mrp.workcenter"]
            .sudo()
            .search([("id", "=", datas.get("service"))])
        )
        from_date = datetime.strptime(datas.get("start_date"), "%Y-%m-%d").strftime(
            "%d/%m/%Y"
        )
        to_date = datetime.strptime(datas.get("end_date"), "%Y-%m-%d").strftime(
            "%d/%m/%Y"
        )
        year_title = datetime.strptime(datas.get("start_date"), "%Y-%m-%d")
        year = str(year_title.year)

        if mp_ids["supplier"]:
            for s in mp_ids["supplier"]:
                sheet = workbook.add_worksheet(s.name)

                title = (
                    title_workcenter["name"]
                    + " "
                    + "Report"
                    + " "
                    + s.name
                    + " "
                    + year
                )

                bold = workbook.add_format({"bold": True})
                format_1 = workbook.add_format(
                    {"bold": True, "align": "center", "bg_color": "yellow", "border": 1}
                )
                format_2 = workbook.add_format({"align": "center", "border": 1})
                format_header = workbook.add_format(
                    {
                        "align": "center",
                        "valign": "vcenter",
                        "bold": True,
                        "size": 12,
                        "top": 1,
                        "left": 1,
                        "right": 1,
                        "bottom": 1,
                        "text_wrap": True,
                        "font": "arial",
                    }
                )

                sheet.merge_range("A1:N1", title, format_header)
                sheet.merge_range("A2:N2", f"{from_date} - {to_date}", format_header)

                row = 2
                col = 0
                sheet.write(row, col, "No", format_1)
                sheet.write(row, col + 1, "TGL", format_1)
                sheet.write(row, col + 2, "Fabric", format_1)
                if title_workcenter["name"] == "PRINTING":
                    sheet.write(row, col + 3, "Description", format_1)
                    sheet.write(row, col + 5, "Consumption", format_1)

                else:
                    sheet.write(row, col + 3, "Color", format_1)
                    sheet.write(row, col + 5, "T. Meter Need", format_1)
                sheet.write(row, col + 4, "Service", format_1)
                sheet.write(row, col + 6, "Date Out", format_1)
                sheet.write(row, col + 7, "T. Meter Out", format_1)
                sheet.write(row, col + 8, "Customer", format_1)
                sheet.write(row, col + 9, "Style Name", format_1)
                sheet.write(row, col + 10, "Total Received", format_1)
                sheet.write(row, col + 11, "Date", format_1)
                sheet.write(row, col + 12, "Keterangan", format_1)
                sheet.write(row, col + 13, "Supplier", format_1)

                no = 1
                row += 1

                mrp_ids = (
                    self.env["mrp.workorder"]
                    .sudo()
                    .search(
                        [
                            ("po_date", ">=", datas.get("start_date")),
                            ("po_date", "<=", datas.get("end_date")),
                            ("state", "in", ["progress", "ready", "done"]),
                            ("supplier", "=", s.id),
                            ("workcenter_id", "=", datas.get("service")),
                        ]
                    )
                )

                for i in mrp_ids:
                    date = i.po_date.strftime("%d/%m/%Y") if i.po_date else ""
                    in_date = i.in_date.strftime("%d/%m/%Y") if i.out_date else ""
                    out_date = i.out_date.strftime("%d/%m/%Y") if i.out_date else ""
                    fabric = ""
                    total_meter_need = 0
                    total_meter_dyeing = i.total_dyeing
                    total_received = i.order_id.order_line[0].qty_received

                    for fab in i.fabric_id:
                        fabric += fab.product_id.name + " "
                        move_ids = i.production_id.move_raw_ids.filtered(
                            lambda x: x.product_id.id == fab.product_id.id
                        )
                        # total_received = move_ids.purchase_id.qty_received
                        for move in move_ids:
                            received = self.env["purchase.order.line"].search(
                                [
                                    "&",
                                    ("order_id.id", "=", i.order_id.id),
                                    ("product_id.id", "=", move.product_id.id),
                                ]
                            )
                            total_meter_need += move.product_uom_qty
                            # total_received = received.qty_received
                    color = i.color_id.name or ""
                    wo = i.workcenter_id.name or ""
                    product = i.product_tmpl_id.name or ""
                    customer = i.customer or ""
                    keterangan = i.keterangan or ""

                    sheet.write(row, col, no, format_2)
                    sheet.write(row, col + 1, date, format_2)
                    sheet.write(row, col + 2, fabric or "", format_2)
                    sheet.write(row, col + 3, color, format_2)
                    sheet.write(row, col + 4, wo, format_2)
                    sheet.write(row, col + 5, total_meter_need, format_2)
                    sheet.write(row, col + 6, out_date, format_2)
                    sheet.write(row, col + 7, total_meter_dyeing, format_2)
                    sheet.write(row, col + 8, customer, format_2)
                    sheet.write(row, col + 9, product, format_2)
                    sheet.write(row, col + 10, total_received, format_2)
                    sheet.write(row, col + 11, in_date, format_2)
                    sheet.write(row, col + 12, " ", format_2)
                    sheet.write(row, col + 13, keterangan, format_2)
                    row += 1
                    no += 1
        else:
            sheet = workbook.add_worksheet("Report")

            title = title_workcenter["name"] + " " + "Report" + " " + year

            bold = workbook.add_format({"bold": True})
            format_1 = workbook.add_format(
                {"bold": True, "align": "center", "bg_color": "yellow", "border": 1}
            )
            format_2 = workbook.add_format({"align": "center", "border": 1})
            format_header = workbook.add_format(
                {
                    "align": "center",
                    "valign": "vcenter",
                    "bold": True,
                    "size": 12,
                    "top": 1,
                    "left": 1,
                    "right": 1,
                    "bottom": 1,
                    "text_wrap": True,
                    "font": "arial",
                }
            )

            sheet.merge_range("A1:N1", title, format_header)
            sheet.merge_range("A2:N2", f"{from_date} - {to_date}", format_header)

            row = 2
            col = 0
            sheet.write(row, col, "No", format_1)
            sheet.write(row, col + 1, "TGL", format_1)
            sheet.write(row, col + 2, "Fabric", format_1)
            if title_workcenter["name"] == "PRINTING":
                sheet.write(row, col + 3, "Description", format_1)
                sheet.write(row, col + 5, "Consumption", format_1)

            else:
                sheet.write(row, col + 3, "Color", format_1)
                sheet.write(row, col + 5, "T. Meter Need", format_1)
            sheet.write(row, col + 4, "Service", format_1)
            sheet.write(row, col + 6, "Date Out", format_1)
            sheet.write(row, col + 7, "T. Meter Out", format_1)
            sheet.write(row, col + 8, "Customer", format_1)
            sheet.write(row, col + 9, "Style Name", format_1)
            sheet.write(row, col + 10, "Total Received", format_1)
            sheet.write(row, col + 11, "Date", format_1)
            sheet.write(row, col + 12, "Keterangan", format_1)
            sheet.write(row, col + 13, "Supplier", format_1)

            no = 1
            row += 1

            mrp_ids = (
                self.env["mrp.workorder"]
                .sudo()
                .search(
                    [
                        ("po_date", ">=", datas.get("start_date")),
                        ("po_date", "<=", datas.get("end_date")),
                        ("state", "in", ["progress", "ready", "done"]),
                        ("workcenter_id", "=", datas.get("service")),
                    ]
                )
            )

            for i in mrp_ids:
                date = i.po_date.strftime("%d/%m/%Y") if i.po_date else ""
                in_date = i.in_date.strftime("%d/%m/%Y") if i.out_date else ""
                out_date = i.out_date.strftime("%d/%m/%Y") if i.out_date else ""
                fabric = ""
                total_meter_need = 0
                total_meter_dyeing = i.total_dyeing
                total_received = i.order_id.order_line[0].qty_received
                for fab in i.fabric_id:
                    fabric += fab.product_id.name + " "
                    move_ids = i.production_id.move_raw_ids.filtered(
                        lambda x: x.product_id.id == fab.product_id.id
                    )
                    # total_received = move_ids.purchase_id.qty_received
                    for move in move_ids:
                        received = self.env["purchase.order.line"].search(
                            [
                                "&",
                                ("order_id.id", "=", i.order_id.id),
                                ("product_id.id", "=", move.product_id.id),
                            ]
                        )
                        total_meter_need += move.product_uom_qty
                        # total_received = received.qty_received
                color = i.color_id.name or ""
                wo = i.workcenter_id.name or ""
                product = i.product_tmpl_id.name or ""
                customer = i.customer or ""
                keterangan = i.supplier.name or ""

                sheet.write(row, col, no, format_2)
                sheet.write(row, col + 1, date, format_2)
                sheet.write(row, col + 2, fabric or "", format_2)
                sheet.write(row, col + 3, color, format_2)
                sheet.write(row, col + 4, wo, format_2)
                sheet.write(row, col + 5, total_meter_need, format_2)
                sheet.write(row, col + 6, out_date, format_2)
                sheet.write(row, col + 7, total_meter_dyeing, format_2)
                sheet.write(row, col + 8, customer, format_2)
                sheet.write(row, col + 9, product, format_2)
                sheet.write(row, col + 10, total_received, format_2)
                sheet.write(row, col + 11, in_date, format_2)
                sheet.write(row, col + 12, " ", format_2)
                sheet.write(row, col + 13, keterangan, format_2)
                row += 1
                no += 1
