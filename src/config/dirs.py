# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""A module containing a set of the project's base directories."""

from __future__ import annotations

__all__: typing.Sequence[str] = ("BLOGS_DIR", "BASE_DIR")

import pathlib
import typing

BASE_DIR = pathlib.Path(__file__).parent.parent
"""The root directory (src) of the project."""

BLOGS_DIR = BASE_DIR / "modules" / "blog" / "application" / "sources"
"""
The directory where corresponding views in PDF format will be saved 
or deleted when blog models are saved or deleted.
"""
