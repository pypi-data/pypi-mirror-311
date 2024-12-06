import httpx


class ScrapedCompanyPage:
    def __init__(self, company_pages_base_url=None):
        self.company_pages_base_url = (
            company_pages_base_url or "https://app.delphai.com/service/company-pages"
        )
        self.http_client = httpx.AsyncClient()

    async def list_domains(self, prefix: str, limit: int = 20):
        endpoint_url = (
            self.company_pages_base_url + "/delphai.CompanyPages.list_domains"
        )
        response = await self.http_client.post(
            endpoint_url, json={"prefix": prefix, "limit": limit}
        )
        response.raise_for_status()
        return response.json()

    async def list_pages(self, domain: str):
        endpoint_url = self.company_pages_base_url + "/delphai.CompanyPages.list_urls"
        response = await self.http_client.post(endpoint_url, json={"domain": domain})
        response.raise_for_status()
        return response.json()

    async def get_content_for_class(
        self,
        content_type: str,
        domain: str = None,
        company_id: str = None,
        page_classes: list = None,
        classifier: str = None,
        language: str = None,
    ):
        request = {}
        request["type"] = content_type

        if domain or company_id:
            if domain:
                request["domain"] = domain
            if company_id:
                request["company_id"] = company_id
        else:
            raise ValueError("Should provide a domain or a company_id.")

        if page_classes:
            request["page_classes"] = page_classes
        if classifier:
            request["classifier"] = classifier
        if language:
            request["language"] = language

        endpoint_url = self.company_pages_base_url + "/delphai.CompanyPages.pages_v3"
        response = await self.http_client.post(endpoint_url, json=request)
        response.raise_for_status()
        page_list = response.json()
        return page_list, len(page_list)

    async def get_page_metadata(self, url: str, domain: str):
        endpoint_url = (
            self.company_pages_base_url + "/delphai.CompanyPages.get_page_metadata"
        )
        response = await self.http_client.post(
            endpoint_url, json={"url": url, "domain": domain}
        )
        response.raise_for_status()
        return response.json()

    async def get_page_content(self, url: str, content_type: str, language: str = None):
        request = {}
        request["url"] = url
        request["type"] = content_type
        if language:
            request["language"] = language

        endpoint_url = self.company_pages_base_url + "/delphai.CompanyPages.page"
        response = await self.http_client.post(endpoint_url, json=request)
        response.raise_for_status()
        return response.json()
