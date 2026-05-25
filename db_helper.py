import sqlite3
import logging
from datetime import datetime, timedelta

db_path = "./imtiaz_crm.db"
RUN_TESTS = False  # set True to run unit tests

# Logger Setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("complaint_agent")

def search_complaint(order_id: str):
    logger.info(f"Searching complaint for Order ID: {order_id}")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # PROCESSED TABLE
        logger.info("Checking PROCESSED table")

        cursor.execute("""
            SELECT tickets, order_id, delivery_date, claim_date,
                   n_days_lapsed, decision, reason
            FROM user_complaint_processed
            WHERE order_id = ?
        """, (order_id,))

        row = cursor.fetchone()

        if row:
            logger.info(f"Found in PROCESSED: {order_id}")

            return {
                "status": "PROCESSED",
                "tickets": row[0],
                "order_id": row[1],
                "delivery_date": row[2],
                "claim_date": row[3],
                "n_days_lapsed": row[4],
                "decision": row[5],
                "reason": row[6]
            }
        else:
            # PROCESSED TABLE NOT FOUND
            logger.info(f"No Record for Order ID {order_id} in PROCESSED table")

        # PENDING TABLE
        logger.info("Checking PENDING table")

        cursor.execute("""
            SELECT order_id, complaint_raw_text, created_at
            FROM user_complaint_pending
            WHERE order_id = ?
        """, (order_id,))

        row = cursor.fetchone()

        if row:
            order_id, text, created_at = row

            # safer datetime parsing
            try:
                created_dt = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            except:
                created_dt = datetime.fromisoformat(created_at)

            due_date = created_dt + timedelta(days=7)

            logger.info(f"Found in PENDING: {order_id} | TAT=7 days")

            return {
                "status": "PENDING",
                "order_id": order_id,
                "complaint_raw_text": text,
                "created_at": created_at,
                "TAT_days": 7,
                "due_date": due_date.strftime("%Y-%m-%d %H:%M:%S")
            }

        else:
            # PROCESSED TABLE NOT FOUND
            logger.info(f"No Record for Order ID {order_id} in PENDING table")

        logger.warning(f"NOT FOUND: {order_id}")

        return {
            "status": "NOT_FOUND",
            "order_id": order_id
        }

    except Exception as e:
        logger.exception(f"Error while searching complaint: {e}")
        return {
            "status": "ERROR",
            "technical_message": str(e),
            "user_message": "We are sorry, we are currently experiencing technical difficulties with our servers. Please try again later."
        }

    finally:
        if 'conn' in locals():
            conn.close()

def register_pending_complaint(order_id: str, complaint_raw_text: str):

    logger.info(f"Registering complaint: {order_id}")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # ⏰ current time
        created_at = datetime.now()
        due_date = created_at + timedelta(days=7)

        cursor.execute("""
            INSERT INTO user_complaint_pending (order_id, complaint_raw_text)
            VALUES (?, ?)
        """, (
            order_id,
            complaint_raw_text
        ))

        conn.commit()

        logger.info(f"Stored in PENDING: {order_id}")
        logger.info(f"TAT=7 days | Due Date: {due_date}")

        return {
            "status": "SUCCESS",
            "order_id": order_id,
            "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "TAT_days": 7,
            "due_date": due_date.strftime("%Y-%m-%d %H:%M:%S"),
            "message": f"Complaint for {order_id} added to pending queue"
        }

    except Exception as e:
        logger.exception(f"Error inserting complaint: {e}")
        return {
            "status": "ERROR",
            "technical_message": str(e),
            "user_message": "We are sorry, we are currently experiencing technical difficulties with our servers. Please try again later."
        }

    finally:
        if 'conn' in locals():
            conn.close()
            
            
            
# --------- UNIT TEST -----------

class ComplaintUnitTest:

    def __init__(self):
        self.test_order_id = "PK-UNIT-TEST-99999"

    def test_insert(self):
        print("\nTEST 1: INSERT")

        result = register_pending_complaint(
            self.test_order_id,
            "Unit test complaint"
        )

        print(result)
        assert result["status"] == "SUCCESS"
        print("Insert passed")

    def test_search(self):
        print("\nTEST 2: SEARCH")

        result = search_complaint(self.test_order_id)

        print(result)
        assert result["order_id"] == self.test_order_id
        print("Search passed")

    def test_cleanup(self):
        print("\nTEST 3: CLEANUP")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM user_complaint_pending
            WHERE order_id = ?
        """, (self.test_order_id,))

        conn.commit()
        conn.close()

        print("Deleted test data")
        print("Cleanup passed")

    def run_all(self):
        print("\n==============================")
        print("UNIT TEST SUITE START")
        print("==============================")

        self.test_insert()
        self.test_search()
        self.test_cleanup()

        print("\nALL TESTS PASSED")

# =========================
# MAIN ENTRY
# =========================

if __name__ == "__main__":

    if RUN_TESTS:
        ComplaintUnitTest().run_all()
    else:
        print("Database Service Loaded Successfully")